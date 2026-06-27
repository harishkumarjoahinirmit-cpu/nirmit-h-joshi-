document.getElementById('scanForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const url = document.getElementById('urlInput').value;
    const scanResults = document.getElementById('scanResults');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const errorMessage = document.getElementById('errorMessage');
    
    // Show loading spinner
    loadingSpinner.style.display = 'flex';
    scanResults.style.display = 'none';
    errorMessage.style.display = 'none';
    
    try {
        const response = await fetch('/api/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayResults(data);
        } else {
            showError(data.error || 'Scan failed');
        }
    } catch (error) {
        showError('Error: ' + error.message);
    } finally {
        loadingSpinner.style.display = 'none';
    }
});

function displayResults(data) {
    // Update security score
    document.getElementById('scoreValue').textContent = Math.round(data.security_score);
    
    // Update SSL info
    const sslInfo = document.getElementById('sslInfo');
    if (data.ssl_info.valid) {
        sslInfo.innerHTML = `
            <div class="info-item">
                <strong>Status:</strong> Valid
            </div>
            <div class="info-item">
                <strong>Version:</strong> ${data.ssl_info.version || 'N/A'}
            </div>
            <div class="info-item">
                <strong>Cipher:</strong> ${data.ssl_info.cipher || 'N/A'}
            </div>
            <div class="info-item">
                <strong>Cipher Bits:</strong> ${data.ssl_info.cipher_bits || 'N/A'}
            </div>
        `;
    } else {
        sslInfo.innerHTML = `<div class="info-item" style="background: #ffe0e0; border-left-color: #ff6b6b;"><strong>Error:</strong> ${data.ssl_info.error || 'Certificate check failed'}</div>`;
    }
    
    // Update open ports
    const portsInfo = document.getElementById('portsInfo');
    if (data.open_ports.length > 0) {
        portsInfo.innerHTML = data.open_ports.map(port => 
            `<div class="port-item"><strong>Port ${port.port}:</strong> ${port.state} (${port.service})</div>`
        ).join('');
    } else {
        portsInfo.innerHTML = '<div class="info-item">No open ports detected</div>';
    }
    
    // Update vulnerabilities
    const vulnInfo = document.getElementById('vulnerabilityInfo');
    if (data.vulnerabilities.length > 0) {
        vulnInfo.innerHTML = data.vulnerabilities.map(vuln => 
            `<div class="vulnerability-item"><i class="fas fa-exclamation-circle"></i> ${vuln}</div>`
        ).join('');
    } else {
        vulnInfo.innerHTML = '<div class="info-item" style="background: #e0ffe0; border-left-color: #51cf66;">No major vulnerabilities detected</div>';
    }
    
    // Update headers
    const headersInfo = document.getElementById('headersInfo');
    if (Object.keys(data.headers_info).length > 0) {
        const headersList = Object.entries(data.headers_info).slice(0, 5);
        headersInfo.innerHTML = headersList.map(([key, value]) => 
            `<div class="info-item"><strong>${key}:</strong> <small>${value}</small></div>`
        ).join('');
    } else {
        headersInfo.innerHTML = '<div class="info-item">No headers info available</div>';
    }
    
    // Show results
    document.getElementById('scanResults').style.display = 'block';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}