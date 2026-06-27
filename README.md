# Vulnerability Scanner Web Application

A comprehensive web-based tool for scanning websites and analyzing security vulnerabilities.

## Features

✅ **URL Scanning** - Scan any website for security issues  
✅ **Open Port Detection** - Identify open ports using Nmap  
✅ **HTTP Header Analysis** - Check for security headers  
✅ **SSL Certificate Checking** - Validate SSL/TLS configurations  
✅ **Security Score Generation** - Get an overall security rating  
✅ **Scan History Dashboard** - View and manage previous scans  
✅ **Real-time Vulnerability Reports** - Detailed security analysis  

## Technology Stack

- **Backend**: Python with Flask
- **Database**: SQLite
- **Scanning Tools**: Nmap, python-nmap
- **Frontend**: HTML5, CSS3, JavaScript
- **Security Libraries**: PyOpenSSL, ssl, certifi

## Installation

### Prerequisites

- Python 3.7+
- Nmap installed on your system
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/harishkumarjoahinirmit-cpu/nirmit-h-joshi-.git
   cd nirmit-h-joshi-
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Nmap**
   - **Ubuntu/Debian**: `sudo apt-get install nmap`
   - **macOS**: `brew install nmap`
   - **Windows**: Download from https://nmap.org/download.html

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`

## Usage

### Scanning a Website

1. Navigate to the home page
2. Enter a website URL (e.g., `https://example.com`)
3. Click "Start Scan"
4. Wait for the scan to complete
5. Review the security report

### Dashboard

- View all previous scans
- Click "View" to see detailed scan results
- Click "Delete" to remove scan records
- Click "Refresh" to update the dashboard

## Features Explained

### Security Score
- Ranges from 0-100
- Deducted points for:
  - Weak SSL/TLS versions
  - Weak cipher suites
  - Missing security headers
  - Open ports

### Vulnerabilities Detected
- Missing security headers (HSTS, CSP, X-Frame-Options, etc.)
- Weak SSL/TLS versions
- Weak cipher suites
- Certificate validation issues

### Open Ports
- Scans ports 1-1000
- Shows port number, state, and service name
- Helps identify exposed services

### Security Headers
- Checks for important HTTP security headers
- Includes: HSTS, CSP, X-Content-Type-Options, X-Frame-Options, X-XSS-Protection

## API Endpoints

### POST /api/scan
Initiate a website scan
```json
{
  "url": "https://example.com"
}
```

### GET /api/results
Retrieve all scan results

### GET /api/results/<scan_id>
Get specific scan result details

### DELETE /api/results/<scan_id>
Delete a scan record

## Database Schema

### ScanResult Table
- `id` - Primary key
- `website_url` - Scanned URL
- `security_score` - Overall security rating
- `scan_date` - When the scan was performed
- `open_ports` - JSON array of open ports
- `ssl_info` - SSL/TLS certificate information
- `headers_info` - HTTP headers analyzed
- `vulnerabilities` - List of found vulnerabilities
- `status` - Scan status

## Security Considerations

⚠️ **Important Notes:**
- Only scan websites you own or have permission to scan
- Nmap scanning may trigger security alerts
- Use responsibly and legally
- Keep the application behind authentication in production
- Use HTTPS in production
- Change the SECRET_KEY in app.py

## Troubleshooting

### Nmap not found
- Ensure Nmap is installed and in your system PATH
- Restart your terminal after installing Nmap

### SSL verification errors
- Check your internet connection
- Verify the website is accessible
- Try with HTTPS URL

### Port scanning takes too long
- Reduce the port range in the code
- Check your network connectivity
- Nmap may require elevated privileges

## Future Enhancements

- [ ] User authentication
- [ ] Scheduled scans
- [ ] Email notifications
- [ ] Advanced vulnerability database
- [ ] API key management
- [ ] Scan result export (PDF, CSV)
- [ ] Custom scan profiles
- [ ] Multi-threaded scanning
- [ ] Enhanced reporting

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on GitHub.

## Disclaimer

This tool is for educational and authorized security testing only. Unauthorized access to computer systems is illegal. Always obtain proper authorization before scanning any website.
