async function loadScanResults() {
    try {
        const response = await fetch('/api/results');
        const results = await response.json();
        
        const tbody = document.getElementById('resultsBody');
        const noResults = document.getElementById('noResults');
        
        if (results.length === 0) {
            noResults.style.display = 'block';
            document.getElementById('dashboardContent').style.display = 'none';
            return;
        }
        
        document.getElementById('dashboardContent').style.display = 'block';
        noResults.style.display = 'none';
        
        tbody.innerHTML = results.map(result => `
            <tr>
                <td><strong>${result.website_url}</strong></td>
                <td>
                    <span class="score-badge ${getScoreBadgeClass(result.security_score)}">
                        ${result.security_score}%
                    </span>
                </td>
                <td>${result.scan_date}</td>
                <td><span class="status-badge">${result.status}</span></td>
                <td>
                    <div class="action-buttons">
                        <button class="btn-view" onclick="showDetails(${result.id})">View</button>
                        <button class="btn-delete" onclick="deleteResult(${result.id})">Delete</button>
                    </div>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading results:', error);
    }
}

function getScoreBadgeClass(score) {
    if (score >= 75) return 'score-high';
    if (score >= 50) return 'score-medium';
    return 'score-low';
}

async function showDetails(scanId) {
    try {
        const response = await fetch(`/api/results/${scanId}`);
        const result = await response.json();
        
        const modal = document.getElementById('detailModal');
        const modalTitle = document.getElementById('modalTitle');
        const modalBody = document.getElementById('modalBody');
        
        modalTitle.textContent = `Scan Details: ${result.website_url}`;
        
        modalBody.innerHTML = `
            <div class="detail-card" style="margin-bottom: 20px;">
                <h4>Security Score: <span style="color: #667eea; font-size: 1.5rem;">${result.security_score}%</span></h4>
            </div>
            
            <div class="detail-card">
                <h4>Vulnerabilities Found:</h4>
                <div>${result.vulnerabilities.length > 0 ? result.vulnerabilities.map(v => `<div class="vulnerability-item">${v}</div>`).join('') : '<p>No vulnerabilities found</p>'}</div>
            </div>
            
            <div class="detail-card">
                <h4>Open Ports:</h4>
                <div>${result.open_ports.length > 0 ? result.open_ports.map(p => `<div class="port-item">Port ${p.port} - ${p.state}</div>`).join('') : '<p>No open ports</p>'}</div>
            </div>
            
            <div class="detail-card">
                <h4>SSL/TLS Info:</h4>
                <div>${JSON.stringify(result.ssl_info).replace(/,/g, '<br>').replace(/[{}"]/g, '')}</div>
            </div>
        `;
        
        modal.style.display = 'flex';
    } catch (error) {
        console.error('Error loading details:', error);
    }
}

async function deleteResult(scanId) {
    if (confirm('Are you sure you want to delete this scan result?')) {
        try {
            await fetch(`/api/results/${scanId}`, { method: 'DELETE' });
            loadScanResults();
        } catch (error) {
            console.error('Error deleting result:', error);
        }
    }
}

document.getElementById('refreshBtn').addEventListener('click', loadScanResults);

document.querySelector('.close-btn').addEventListener('click', () => {
    document.getElementById('detailModal').style.display = 'none';
});

window.addEventListener('click', (e) => {
    const modal = document.getElementById('detailModal');
    if (e.target === modal) {
        modal.style.display = 'none';
    }
});

// Load results on page load
loadScanResults();