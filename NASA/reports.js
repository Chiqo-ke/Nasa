const API_URL = 'http://localhost:8000';
let allReports = [];
let currentReportId = null;
let currentFilter = 'all';

// Load reports on page load
window.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }
    loadReports();
});

async function loadReports() {
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await fetch(`${API_URL}/reports`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            if (response.status === 403) {
                alert('Access Denied: Only Finance Office can access reports');
                window.location.href = 'index.html';
                return;
            }
            throw new Error('Failed to load reports');
        }

        const data = await response.json();
        allReports = data.reports;
        
        // Update statistics
        document.getElementById('totalReports').textContent = data.total_reports;
        document.getElementById('pendingReports').textContent = data.pending_count;
        document.getElementById('reviewedReports').textContent = data.reviewed_count;
        document.getElementById('resolvedReports').textContent = data.resolved_count;
        
        // Display reports
        displayReports(allReports);
    } catch (error) {
        console.error('Error loading reports:', error);
        document.getElementById('reportsTable').innerHTML = `
            <tr>
                <td colspan="7" class="px-6 py-8 text-center text-red-500">
                    <i class="fas fa-exclamation-circle text-2xl mb-2"></i>
                    <p>Error loading reports</p>
                </td>
            </tr>
        `;
    }
}

function displayReports(reports) {
    const tableBody = document.getElementById('reportsTable');
    
    if (reports.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" class="px-6 py-8 text-center text-gray-500">
                    <i class="fas fa-inbox text-4xl mb-2"></i>
                    <p>No reports found</p>
                </td>
            </tr>
        `;
        return;
    }

    tableBody.innerHTML = reports.map(report => `
        <tr class="hover:bg-gray-50 cursor-pointer" onclick="viewReport(${report.id})">
            <td class="px-6 py-4 text-sm font-medium text-gray-900">#${report.id}</td>
            <td class="px-6 py-4 text-sm text-gray-600">${formatDate(report.created_at)}</td>
            <td class="px-6 py-4 text-sm">
                <span class="px-2 py-1 rounded-full text-xs font-semibold ${report.report_type === 'tax_payment' ? 'bg-purple-100 text-purple-800' : 'bg-green-100 text-green-800'}">
                    ${report.report_type === 'tax_payment' ? 'Tax Payment' : 'Citizen Portal'}
                </span>
            </td>
            <td class="px-6 py-4 text-sm text-gray-900">${report.reported_by}</td>
            <td class="px-6 py-4 text-sm text-gray-900">${report.subject}</td>
            <td class="px-6 py-4 text-sm">
                <span class="status-badge status-${report.status}">
                    ${report.status.charAt(0).toUpperCase() + report.status.slice(1)}
                </span>
            </td>
            <td class="px-6 py-4 text-sm">
                <button onclick="event.stopPropagation(); viewReport(${report.id})" class="text-blue-600 hover:text-blue-800 font-semibold">
                    <i class="fas fa-eye mr-1"></i>View
                </button>
            </td>
        </tr>
    `).join('');
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function filterReports(status) {
    currentFilter = status;
    
    // Update button styles
    document.querySelectorAll('.filter-btn').forEach(btn => {
        if (btn.dataset.filter === status) {
            btn.className = 'filter-btn px-6 py-2 bg-blue-500 text-white rounded-lg';
        } else {
            btn.className = 'filter-btn px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300';
        }
    });
    
    // Filter reports
    const filtered = status === 'all' 
        ? allReports 
        : allReports.filter(r => r.status === status);
    
    displayReports(filtered);
}

function viewReport(reportId) {
    const report = allReports.find(r => r.id === reportId);
    if (!report) return;
    
    currentReportId = reportId;
    
    const detailsHtml = `
        <div class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <p class="text-sm text-gray-500">Report ID</p>
                    <p class="font-semibold">#${report.id}</p>
                </div>
                <div>
                    <p class="text-sm text-gray-500">Date Submitted</p>
                    <p class="font-semibold">${formatDate(report.created_at)}</p>
                </div>
                <div>
                    <p class="text-sm text-gray-500">Report Type</p>
                    <p class="font-semibold">${report.report_type === 'tax_payment' ? 'Tax Payment' : 'Citizen Portal'}</p>
                </div>
                <div>
                    <p class="text-sm text-gray-500">Status</p>
                    <span class="status-badge status-${report.status}">
                        ${report.status.charAt(0).toUpperCase() + report.status.slice(1)}
                    </span>
                </div>
            </div>
            
            <div>
                <p class="text-sm text-gray-500">Reported By</p>
                <p class="font-semibold">${report.reported_by}</p>
            </div>
            
            <div>
                <p class="text-sm text-gray-500">Subject</p>
                <p class="font-semibold text-lg">${report.subject}</p>
            </div>
            
            <div>
                <p class="text-sm text-gray-500">Description</p>
                <p class="text-gray-700 bg-gray-50 p-4 rounded-lg">${report.description}</p>
            </div>
            
            ${report.transaction_hash ? `
                <div>
                    <p class="text-sm text-gray-500">Transaction Hash</p>
                    <code class="text-xs bg-gray-100 px-2 py-1 rounded block break-all">${report.transaction_hash}</code>
                </div>
            ` : ''}
            
            ${report.reviewed_by ? `
                <div>
                    <p class="text-sm text-gray-500">Reviewed By</p>
                    <p class="font-semibold">${report.reviewed_by}</p>
                </div>
            ` : ''}
            
            ${report.admin_notes ? `
                <div>
                    <p class="text-sm text-gray-500">Admin Notes</p>
                    <p class="text-gray-700 bg-blue-50 p-4 rounded-lg">${report.admin_notes}</p>
                </div>
            ` : ''}
        </div>
    `;
    
    document.getElementById('reportDetails').innerHTML = detailsHtml;
    document.getElementById('updateStatus').value = report.status;
    document.getElementById('adminNotes').value = report.admin_notes || '';
    
    // Show modal and prevent body scrolling
    const modal = document.getElementById('reportModal');
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeReportModal() {
    document.getElementById('reportModal').classList.add('hidden');
    document.body.style.overflow = 'auto'; // Re-enable scrolling on body
    currentReportId = null;
}

// Close modal when clicking on backdrop
function closeModalOnBackdrop(event) {
    if (event.target.id === 'reportModal') {
        closeReportModal();
    }
}

// Close modal with Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const modal = document.getElementById('reportModal');
        if (modal && !modal.classList.contains('hidden')) {
            closeReportModal();
        }
    }
});

async function updateReport() {
    if (!currentReportId) return;
    
    const status = document.getElementById('updateStatus').value;
    const adminNotes = document.getElementById('adminNotes').value.trim();
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await fetch(`${API_URL}/reports/${currentReportId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                status: status,
                admin_notes: adminNotes
            })
        });

        if (!response.ok) {
            throw new Error('Failed to update report');
        }

        alert('Report updated successfully!');
        closeReportModal();
        loadReports(); // Reload reports
    } catch (error) {
        console.error('Error updating report:', error);
        alert('Failed to update report. Please try again.');
    }
}

// Auto-refresh every 30 seconds
setInterval(loadReports, 30000);
