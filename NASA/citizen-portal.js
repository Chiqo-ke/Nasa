const backendUrl = 'http://127.0.0.1:8000';

let allTransactions = [];

// Format date
function formatDate(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Truncate wallet address for display
function truncateAddress(address) {
    if (!address) return 'N/A';
    return `${address.substring(0, 8)}...${address.substring(address.length - 6)}`;
}

// Load blockchain data
async function loadBlockchainData() {
    try {
        // Fetch blockchain data from backend
        const response = await fetch(`${backendUrl}/blockchain`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch blockchain data');
        }

        const blockchain = await response.json();
        
        // Extract all transactions from all blocks
        allTransactions = [];
        let totalFunds = 0;
        const uniqueAddresses = new Set();

        blockchain.chain.forEach(block => {
            if (block.transactions && block.transactions.length > 0) {
                block.transactions.forEach(tx => {
                    allTransactions.push({
                        ...tx,
                        timestamp: block.timestamp,
                        block_id: block.block_id,
                        validator: block.validator
                    });
                    totalFunds += parseFloat(tx.amount || 0);
                    uniqueAddresses.add(tx.sender);
                    uniqueAddresses.add(tx.recipient);
                });
            }
        });

        // Update statistics
        document.getElementById('totalTransactions').textContent = allTransactions.length;
        document.getElementById('totalFunds').textContent = totalFunds.toFixed(2);
        document.getElementById('activeOffices').textContent = uniqueAddresses.size;
        document.getElementById('lastUpdate').textContent = formatDate(new Date());

        // Display transactions
        displayTransactions(allTransactions);
    } catch (error) {
        console.error('Error loading blockchain data:', error);
        document.getElementById('transactionsTable').innerHTML = `
            <tr>
                <td colspan="7" class="px-6 py-8 text-center text-red-500">
                    <i class="fas fa-exclamation-triangle text-2xl mb-2"></i>
                    <p>Error loading transactions: ${error.message}</p>
                    <button onclick="loadBlockchainData()" class="mt-4 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
                        Retry
                    </button>
                </td>
            </tr>
        `;
    }
}

// Display transactions in table
function displayTransactions(transactions) {
    const tableBody = document.getElementById('transactionsTable');
    
    if (transactions.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" class="px-6 py-8 text-center text-gray-500">
                    <i class="fas fa-inbox text-4xl mb-3 text-gray-300"></i>
                    <p>No transactions found</p>
                </td>
            </tr>
        `;
        return;
    }

    // Sort by timestamp (newest first)
    const sortedTransactions = [...transactions].sort((a, b) => 
        new Date(b.timestamp) - new Date(a.timestamp)
    );

    tableBody.innerHTML = sortedTransactions.map(tx => `
        <tr class="hover:bg-gray-50 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                ${formatDate(tx.timestamp)}
            </td>
            <td class="px-6 py-4 text-sm text-gray-600">
                <code class="bg-gray-100 px-2 py-1 rounded text-xs">${truncateAddress(tx.sender)}</code>
            </td>
            <td class="px-6 py-4 text-sm text-gray-600">
                <code class="bg-gray-100 px-2 py-1 rounded text-xs">${truncateAddress(tx.recipient)}</code>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-green-600">
                ${parseFloat(tx.amount).toFixed(2)}
            </td>
            <td class="px-6 py-4 text-sm text-gray-900">
                ${tx.purpose || 'Not specified'}
            </td>
            <td class="px-6 py-4 text-sm text-gray-600">
                ${tx.approved_by || 'Not specified'}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                    <i class="fas fa-check-circle mr-1"></i>Verified
                </span>
            </td>
        </tr>
    `).join('');
}

// Search and filter functionality
function filterTransactions() {
    const searchTerm = document.getElementById('searchPurpose').value.toLowerCase();
    const amountFilter = document.getElementById('filterAmount').value;

    let filtered = allTransactions;

    // Filter by purpose
    if (searchTerm) {
        filtered = filtered.filter(tx => 
            (tx.purpose || '').toLowerCase().includes(searchTerm) ||
            (tx.approved_by || '').toLowerCase().includes(searchTerm)
        );
    }

    // Filter by amount
    if (amountFilter !== 'all') {
        filtered = filtered.filter(tx => {
            const amount = parseFloat(tx.amount);
            if (amountFilter === '0-1000') return amount < 1000;
            if (amountFilter === '1000-10000') return amount >= 1000 && amount < 10000;
            if (amountFilter === '10000+') return amount >= 10000;
            return true;
        });
    }

    displayTransactions(filtered);
}

// Event listeners
document.getElementById('searchButton').addEventListener('click', filterTransactions);
document.getElementById('searchPurpose').addEventListener('keyup', (e) => {
    if (e.key === 'Enter') filterTransactions();
});
document.getElementById('filterAmount').addEventListener('change', filterTransactions);

// Auto-refresh every 30 seconds
setInterval(loadBlockchainData, 30000);

// Initial load
loadBlockchainData();

// Report Modal Functions
function openReportModal() {
    document.getElementById('reportModal').classList.remove('hidden');
}

function closeReportModal() {
    document.getElementById('reportModal').classList.add('hidden');
    document.getElementById('reporterName').value = '';
    document.getElementById('reportSubject').value = '';
    document.getElementById('reportDescription').value = '';
    document.getElementById('reportTxHash').value = '';
    document.getElementById('reportMessage').classList.add('hidden');
}

async function submitReport() {
    const reporterName = document.getElementById('reporterName').value.trim();
    const subject = document.getElementById('reportSubject').value.trim();
    const description = document.getElementById('reportDescription').value.trim();
    const txHash = document.getElementById('reportTxHash').value.trim();

    // Validation
    if (!reporterName) {
        showReportMessage('Please enter your name or email', 'error');
        return;
    }

    if (!subject) {
        showReportMessage('Please enter a subject', 'error');
        return;
    }

    if (!description) {
        showReportMessage('Please provide a detailed description', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/reports`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                report_type: 'citizen_portal',
                reported_by: reporterName,
                subject: subject,
                description: description,
                transaction_hash: txHash || null
            })
        });

        const result = await response.json();

        if (response.ok) {
            showReportMessage('Report submitted successfully! Your report ID is: ' + result.report_id, 'success');
            setTimeout(() => {
                closeReportModal();
            }, 3000);
        } else {
            showReportMessage(result.detail || 'Failed to submit report', 'error');
        }
    } catch (error) {
        console.error('Error submitting report:', error);
        showReportMessage('An error occurred while submitting the report', 'error');
    }
}

function showReportMessage(message, type) {
    const messageEl = document.getElementById('reportMessage');
    messageEl.textContent = message;
    messageEl.className = `mb-4 p-4 rounded-lg ${type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`;
    messageEl.classList.remove('hidden');
}
