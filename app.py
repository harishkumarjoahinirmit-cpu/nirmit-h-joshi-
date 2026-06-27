from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import nmap
import socket
import ssl
import requests
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vulnerability_scanner.db'
app.config['SECRET_KEY'] = 'your-secret-key-here'
db = SQLAlchemy(app)

# Database Models
class ScanResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website_url = db.Column(db.String(255), nullable=False)
    security_score = db.Column(db.Float, default=0)
    scan_date = db.Column(db.DateTime, default=datetime.utcnow)
    open_ports = db.Column(db.Text)
    ssl_info = db.Column(db.Text)
    headers_info = db.Column(db.Text)
    vulnerabilities = db.Column(db.Text)
    status = db.Column(db.String(50))

    def to_dict(self):
        return {
            'id': self.id,
            'website_url': self.website_url,
            'security_score': self.security_score,
            'scan_date': self.scan_date.strftime('%Y-%m-%d %H:%M:%S'),
            'open_ports': json.loads(self.open_ports) if self.open_ports else [],
            'ssl_info': json.loads(self.ssl_info) if self.ssl_info else {},
            'headers_info': json.loads(self.headers_info) if self.headers_info else {},
            'vulnerabilities': json.loads(self.vulnerabilities) if self.vulnerabilities else [],
            'status': self.status
        }

# Security Scanner Class
class VulnerabilityScanner:
    def __init__(self, url):
        self.url = url
        self.domain = self._extract_domain(url)
        self.vulnerabilities = []
        self.security_score = 100
        self.open_ports = []
        self.ssl_info = {}
        self.headers_info = {}

    def _extract_domain(self, url):
        """Extract domain from URL"""
        url = url.replace('http://', '').replace('https://', '')
        return url.split('/')[0]

    def scan_ports(self):
        """Detect open ports using Nmap"""
        try:
            nm = nmap.PortScanner()
            nm.scan(self.domain, '1-1000')
            
            for host in nm.all_hosts():
                for proto in nm[host].all_protocols():
                    ports = nm[host][proto].keys()
                    for port in ports:
                        if nm[host][proto][port]['state'] == 'open':
                            self.open_ports.append({
                                'port': port,
                                'state': 'open',
                                'service': nm[host][proto][port].get('name', 'unknown')
                            })
                            # Deduct security score for each open port
                            self.security_score -= 2
        except Exception as e:
            print(f"Port scanning error: {str(e)}")

    def check_ssl_certificate(self):
        """Check SSL/TLS certificate configuration"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    
                    self.ssl_info = {
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'version': ssock.version(),
                        'cipher': cipher[0],
                        'cipher_bits': cipher[2],
                        'valid': True
                    }
                    
                    # Check SSL version
                    if 'TLSv1.2' not in ssock.version() and 'TLSv1.3' not in ssock.version():
                        self.vulnerabilities.append('Weak SSL/TLS version detected')
                        self.security_score -= 15
                    
                    # Check cipher strength
                    if cipher[2] < 128:
                        self.vulnerabilities.append('Weak cipher suite detected')
                        self.security_score -= 10
        except Exception as e:
            self.ssl_info['valid'] = False
            self.ssl_info['error'] = str(e)
            self.vulnerabilities.append('SSL/TLS certificate check failed')
            self.security_score -= 20

    def check_http_headers(self):
        """Analyze HTTP security headers"""
        try:
            url = self.url if self.url.startswith('http') else f'https://{self.url}'
            response = requests.get(url, timeout=10, verify=False)
            headers = response.headers
            
            self.headers_info = dict(headers)
            
            # Security headers to check
            required_headers = {
                'Strict-Transport-Security': 'HSTS',
                'X-Content-Type-Options': 'X-Content-Type-Options',
                'X-Frame-Options': 'Clickjacking Protection',
                'X-XSS-Protection': 'XSS Protection',
                'Content-Security-Policy': 'CSP',
                'Referrer-Policy': 'Referrer-Policy'
            }
            
            for header, description in required_headers.items():
                if header not in headers:
                    self.vulnerabilities.append(f'Missing security header: {description}')
                    self.security_score -= 5
        except Exception as e:
            print(f"Header check error: {str(e)}")

    def perform_full_scan(self):
        """Execute complete vulnerability scan"""
        self.check_ssl_certificate()
        self.check_http_headers()
        self.scan_ports()
        
        # Ensure score stays between 0-100
        self.security_score = max(0, min(100, self.security_score))
        
        return {
            'security_score': self.security_score,
            'vulnerabilities': self.vulnerabilities,
            'open_ports': self.open_ports,
            'ssl_info': self.ssl_info,
            'headers_info': self.headers_info
        }

# Routes
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/api/scan', methods=['POST'])
def scan_website():
    """API endpoint for scanning website"""
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        scanner = VulnerabilityScanner(url)
        results = scanner.perform_full_scan()
        
        # Store results in database
        scan_result = ScanResult(
            website_url=url,
            security_score=results['security_score'],
            open_ports=json.dumps(results['open_ports']),
            ssl_info=json.dumps(results['ssl_info']),
            headers_info=json.dumps(list(results['headers_info'].items())),
            vulnerabilities=json.dumps(results['vulnerabilities']),
            status='completed'
        )
        db.session.add(scan_result)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'scan_id': scan_result.id,
            'website': url,
            'security_score': results['security_score'],
            'vulnerabilities': results['vulnerabilities'],
            'open_ports': results['open_ports'],
            'ssl_info': results['ssl_info'],
            'headers_info': dict(results['headers_info'])
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'failed'}), 500

@app.route('/api/results/<int:scan_id>', methods=['GET'])
def get_scan_result(scan_id):
    """Get specific scan result"""
    result = ScanResult.query.get(scan_id)
    if not result:
        return jsonify({'error': 'Scan result not found'}), 404
    
    return jsonify(result.to_dict()), 200

@app.route('/api/results', methods=['GET'])
def get_all_results():
    """Get all scan results"""
    results = ScanResult.query.order_by(ScanResult.scan_date.desc()).all()
    return jsonify([result.to_dict() for result in results]), 200

@app.route('/api/results/<int:scan_id>', methods=['DELETE'])
def delete_scan_result(scan_id):
    """Delete scan result"""
    result = ScanResult.query.get(scan_id)
    if not result:
        return jsonify({'error': 'Scan result not found'}), 404
    
    db.session.delete(result)
    db.session.commit()
    return jsonify({'status': 'deleted'}), 200

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)