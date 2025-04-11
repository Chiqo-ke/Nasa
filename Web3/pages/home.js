const API_BASE_URL = 'http://127.0.0.1:8000';
let currentFilter = 'all';

// Utility Functions

// Check authentication
async function checkAuth() {
    const access_token = localStorage.getItem('access_token');
    if (!access_token) {
        window.location.href = '/login.html';
        return null;
    }

    try {
        const parts = access_token.split('.');
        if (parts.length !== 3) {
            localStorage.removeItem('access_token');
            window.location.href = '/login.html';
            return null;
        }

        const payload = JSON.parse(atob(parts[1]));
        const currentTime = Math.floor(Date.now() / 1000);
        if (payload.exp && payload.exp < currentTime) {
            const newAccessToken = await refreshToken();
            return newAccessToken;
        }
    } catch (e) {
        localStorage.removeItem('access_token');
        window.location.href = '/login.html';
        return null;
    }

    return access_token;
}

// Refresh token
async function refreshToken() {
    const refresh_token = localStorage.getItem('refresh_token');
    if (!refresh_token) {
        window.location.href = '/login.html';
        return null;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/refresh-token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                refresh_token: refresh_token,
            }),
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || 'Token refresh failed');

        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        localStorage.setItem('office_name', data.office_name);
        localStorage.setItem('wallet_address', data.wallet_address);

        return data.access_token;
    } catch (error) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('office_name');
        localStorage.removeItem('wallet_address');
        window.location.href = '/login.html';
        throw error;
    }
}

// Fetch with authentication
async function fetchWithAuth(endpoint, options = {}) {
    let access_token = await checkAuth();
    if (!access_token) return null;

    const defaultOptions = {
        headers: {
            'Authorization': `Bearer ${access_token}`,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        credentials: 'include',
    };

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...(options.headers || {}),
            },
        });

        if (response.status === 401) {
            access_token = await refreshToken();
            if (!access_token) return null;

            defaultOptions.headers['Authorization'] = `Bearer ${access_token}`;

            const retryResponse = await fetch(`${API_BASE_URL}${endpoint}`, {
                ...defaultOptions,
                ...options,
                headers: {
                    ...defaultOptions.headers,
                    ...(options.headers || {}),
                },
            });

            return retryResponse;
        }

        return response;
    } catch (error) {
        console.error(`API call failed for ${endpoint}:`, error);
        throw error;
    }
}

// Handle API responses
async function handleApiResponse(response, errorMessage) {
    if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        console.error('API Error:', {
            status: response.status,
            statusText: response.statusText,
            errorData,
            endpoint: response.url,
        });
        throw new Error(errorData?.detail || errorMessage);
    }
    return response.json();
}

// Fetch user data
async function fetchUserData() {
    try {
        const response = await fetchWithAuth('/me/');
        if (!response) return;

        const data = await handleApiResponse(response, 'Failed to fetch user data');
        document.getElementById('officeName').textContent = data.office_name;
        document.getElementById('walletAddress').textContent = data.wallet_address;
    } catch (error) {
        console.error('User data fetch error:', error);
        showAlert(`Failed to load user data: ${error.message}`);
    }
}

// Fetch balance
async function fetchBalance() {
    try {
        const response = await fetchWithAuth('/balance/');
        if (!response) return;

        const data = await handleApiResponse(response, 'Failed to fetch balance');
        document.getElementById('balance').textContent = data.balance.toFixed(2);
    } catch (error) {
        console.error('Balance fetch error:', error);
        showAlert(`Failed to load balance: ${error.message}`);
    }
}

// Fetch transactions
async function fetchTransactions() {
    const tbody = document.getElementById('transactionsTable');
    tbody.innerHTML = '<tr><td colspan="4" class="px-6 py-4 text-center text-gray-500">Loading transactions...</td></tr>';

    try {
        const response = await fetchWithAuth('/transactions/');
        if (!response) return;

        const data = await handleApiResponse(response, 'Failed to fetch transactions');
        const walletAddress = localStorage.getItem('wallet_address');
        let filteredTx = data.transactions;

        if (currentFilter === 'in') {
            filteredTx = filteredTx.filter(tx => tx.recipient === walletAddress);
        } else if (currentFilter === 'out') {
            filteredTx = filteredTx.filter(tx => tx.sender === walletAddress);
        }

        tbody.innerHTML = filteredTx.length === 0 ?
            '<tr><td colspan="4" class="px-6 py-4 text-center text-gray-500">No transactions found</td></tr>' :
            filteredTx.map(tx => {
                const isReceived = tx.recipient === walletAddress;
                return `
                    <tr>
                        <td class="px-6 py-4 text-sm text-gray-500">${new Date(tx.timestamp).toLocaleString()}</td>
                        <td class="px-6 py-4">
                            <span class="px-2 py-1 rounded-full text-xs font-medium ${isReceived ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'}">
                                ${isReceived ? 'Received' : 'Sent'}
                            </span>
                        </td>
                        <td class="px-6 py-4 text-sm font-mono text-gray-500">${isReceived ? tx.sender : tx.recipient}</td>
                        <td class="px-6 py-4 text-sm font-medium ${isReceived ? 'text-green-600' : 'text-red-600'}">
                            ${isReceived ? '+' : '-'}${tx.amount}
                        </td>
                    </tr>
                `;
            }).join('');
    } catch (error) {
        console.error('Transactions fetch error:', error);
        tbody.innerHTML = '<tr><td colspan="4" class="px-6 py-4 text-center text-red-500">Error loading transactions</td></tr>';
        showAlert(`Failed to load transactions: ${error.message}`);
    }
}

function hideAlert() {
    document.getElementById('alertBanner').classList.add('hidden');
}

// Show alert message
function showAlert(message, type = 'error') {
    const banner = document.getElementById('alertBanner');
    const messageEl = document.getElementById('alertMessage');
    messageEl.textContent = message;

    banner.classList.remove('hidden');

    const borderElement = banner.querySelector('.border-l-4');
    borderElement.classList.remove('border-yellow-400', 'border-red-400', 'border-green-400');

    switch (type) {
        case 'error':
            borderElement.classList.add('border-red-400');
            break;
        case 'success':
            borderElement.classList.add('border-green-400');
            break;
        default:
            borderElement.classList.add('border-yellow-400');
    }

    setTimeout(() => {
        banner.classList.add('hidden');
    }, 5000);
}

// Send transaction
async function sendTransaction(recipientAddress, amount) {
    try {
        const access_token = await checkAuth();
        if (!access_token) return;

        const response = await fetch(`${API_BASE_URL}/send/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${access_token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                recipient: recipientAddress,
                amount: parseFloat(amount),
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Transaction failed');
        }

        showAlert('Transaction completed successfully', 'success');
        await Promise.all([fetchBalance(), fetchTransactions()]);
    } catch (error) {
        console.error('Transaction error:', error);
        showAlert(`Transaction failed: ${error.message}`);
    }
}

// Handle logout
async function handleLogout() {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) {
            alert('No active session found.');
            return;
        }

        const response = await fetch(`${API_BASE_URL}/logout`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        const data = await response.json();
        if (response.ok) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('office_name');
            localStorage.removeItem('wallet_address');
            alert(data.message || 'Successfully logged out');
            window.location.href = '/login.html';
        } else {
            alert(`Logout failed: ${data.message || 'Unknown error'}`);
        }
    } catch (error) {
        console.error('Error during logout:', error);
        alert('An error occurred while logging out. Please try again.');
    }
}

// Load and setup payment modal
async function loadPaymentModal() {
    console.log('Send button clicked, loading payment modal...');

    try {
        const response = await fetch('payment-modal.html');
        if (!response.ok) {
            throw new Error(`Failed to fetch modal: ${response.status} ${response.statusText}`);
        }
        const modalHTML = await response.text();
        console.log('Modal HTML:', modalHTML); // Debugging log
        document.body.insertAdjacentHTML('beforeend', modalHTML);

        // Add event listeners for the modal
        setupModalEventListeners();
    } catch (error) {
        console.error('Error loading payment modal:', error);
        showAlert('Failed to load payment form. Please try again.');
    }
}

// Setup modal event listeners
function setupModalEventListeners() {
    // Close modal when cancel button is clicked
    document.getElementById('cancelSend').addEventListener('click', () => {
        document.getElementById('sendModal').remove();
    });

    // Close modal when clicking outside the modal
    document.getElementById('sendModal').addEventListener('click', (e) => {
        if (e.target === document.getElementById('sendModal')) {
            document.getElementById('sendModal').remove();
        }
    });

    // Handle send transaction
    document.getElementById('confirmSend').addEventListener('click', () => {
        const recipientAddress = document.getElementById('recipientAddress').value.trim();
        const amount = document.getElementById('amount').value.trim();

        if (!recipientAddress || !amount || amount <= 0) {
            showAlert('Please enter valid recipient address and amount');
            return;
        }

        sendTransaction(recipientAddress, amount);
        document.getElementById('sendModal').remove();
    });
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    fetchUserData();
    fetchBalance();
    fetchTransactions();

    document.getElementById('refreshButton').addEventListener('click', fetchTransactions);
    document.getElementById('logoutButton').addEventListener('click', handleLogout);

    // Add event listener for the "Send" button
    document.getElementById('sendButton').addEventListener('click', loadPaymentModal);

    // Copy address functionality
    document.getElementById('copyAddress').addEventListener('click', () => {
        const address = document.getElementById('walletAddress').textContent;
        navigator.clipboard.writeText(address)
            .then(() => showAlert('Address copied to clipboard', 'success'))
            .catch(() => showAlert('Failed to copy address'));
    });

    // Filter buttons
    document.querySelectorAll('[data-filter]').forEach(button => {
        button.addEventListener('click', () => {
            currentFilter = button.dataset.filter;
            document.querySelectorAll('[data-filter]').forEach(btn => {
                btn.classList.remove('bg-yellow-200');
                btn.classList.add('bg-gray-200');
            });
            button.classList.add('bg-yellow-200');
            button.classList.remove('bg-gray-200');
            fetchTransactions();
        });
    });
});



// Global error handling
window.addEventListener('unhandledrejection', function (event) {
    console.error('Unhandled promise rejection:', event.reason);
    if (event.reason instanceof Error) {
        showAlert(`An unexpected error occurred: ${event.reason.message}`);
    } else {
        showAlert('An unexpected error occurred. Please try again.');
    }
});