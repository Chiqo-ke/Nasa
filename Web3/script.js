// Configuration
const API_BASE_URL = 'http://127.0.0.1:8000';
const FRONTEND_URL = 'http://localhost:5500';

// State Management
let transactions = [];
let currentActiveNav = 'national';
let currentFilterType = 'all';

// Navigation Items (if not defined elsewhere)
const navItems = [
    { id: 'national', text: 'National', active: true },
    { id: 'transactions', text: 'Transactions', active: false },
    { id: 'reports', text: 'Reports', active: false }
];

// Fetch Transactions from Backend
async function fetchTransactions() {
    try {
        // Log the start of the fetch attempt
        console.log('Attempting to fetch transactions');

        // Perform the fetch with full configuration
        const response = await fetch('http://127.0.0.1:8000/transactions_all/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                // Optional: Add any additional headers if needed
                // 'Authorization': 'Bearer YOUR_TOKEN_IF_APPLICABLE'
            },
            // Optional: Add credentials if you're using authentication
            // credentials: 'include'
        });

        // Log the response status
        console.log('Response status:', response.status);

        // Check if the response is successful
        if (!response.ok) {
            // Throw an error with detailed status information
            throw new Error(`HTTP error! status: ${response.status}, statusText: ${response.statusText}`);
        }

        // Parse the JSON response
        const data = await response.json();

        // Log the received data
        console.log('Received transactions:', data);

        // Transform backend transactions to frontend format
        transactions = data.transactions_all.map(transaction => ({
            date: new Date().toLocaleString(), // Temporary timestamp
            type: transaction.type === 'incoming' ? 'Received' : 'Sent',
            wallet: transaction.counterparty,
            amount: `$${Math.abs(transaction.amount).toFixed(2)}`
        }));

        // Display the transactions
        displayTransactions();

    } catch (error) {
        // Comprehensive error handling
        console.error('Transaction fetch failed:', error);

        // Provide user-friendly error feedback
        const tbody = document.getElementById("transactionsTableBody");
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="4" class="px-6 py-8 text-center text-red-500">
                        Unable to load transactions. 
                        ${error.message ? `Error: ${error.message}` : 'Please check your connection.'}
                    </td>
                </tr>
            `;
        }

        // Optional: Show a toast or alert to the user
        // You might want to implement a more sophisticated error notification system
        alert('Failed to load transactions. Please try again later.');
    }
}

// Initialize Navigation
function initializeNavigation() {
    const mainNav = document.getElementById('mainNav');
    if (!mainNav) return;
    
    mainNav.innerHTML = navItems.map(item => `
        <button 
            data-nav-id="${item.id}"
            class="px-4 py-3 text-sm font-medium transition-all duration-200 ${
                item.active 
                    ? 'text-gray-700 border-b-2 border-blue-500' 
                    : 'text-gray-500 hover:text-gray-700 border-b-2 border-transparent'
            }"
        >
            ${item.text}
        </button>
    `).join('');

    mainNav.querySelectorAll('button').forEach(button => {
        button.addEventListener('click', () => {
            const navId = button.getAttribute('data-nav-id');
            updateNavigation(navId);
        });
    });
}

// Update Navigation State
function updateNavigation(navId) {
    const mainNav = document.getElementById('mainNav');
    if (!mainNav) return;

    currentActiveNav = navId;
    
    mainNav.querySelectorAll('button').forEach(btn => {
        const btnId = btn.getAttribute('data-nav-id');
        if (btnId === navId) {
            btn.classList.remove('text-gray-500', 'border-transparent');
            btn.classList.add('text-gray-700', 'border-blue-500');
        } else {
            btn.classList.remove('text-gray-700', 'border-blue-500');
            btn.classList.add('text-gray-500', 'border-transparent');
        }
    });
}

// Initialize Filter System
function initializeFilterSystem() {
    const filterContainer = document.querySelector('.filter-container');
    if (!filterContainer) return;

    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            updateFilterButtons(button.id);
        });
    });

    setupAdvancedFilters();
}

// Update Filter Buttons
function updateFilterButtons(filterId) {
    const filterButtons = document.querySelectorAll('.filter-btn');
    currentFilterType = filterId.replace('filter', '').toLowerCase();

    filterButtons.forEach(btn => {
        if (btn.id === filterId) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    applyCurrentFilters();
}

// Setup Advanced Filters
function setupAdvancedFilters() {
    const advancedFilterButton = document.querySelector('.advanced-filter-button');
    const advancedFilterForm = document.getElementById('advancedFilterForm');
    
    if (advancedFilterButton && advancedFilterForm) {
        // Toggle form visibility
        advancedFilterButton.addEventListener('click', (e) => {
            e.stopPropagation();
            advancedFilterForm.classList.toggle('hidden');
        });

        // Close form when clicking outside
        document.addEventListener('click', (e) => {
            if (!advancedFilterForm.contains(e.target) && 
                !advancedFilterButton.contains(e.target)) {
                advancedFilterForm.classList.add('hidden');
            }
        });

        // Handle form submission
        advancedFilterForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(advancedFilterForm);
            handleAdvancedFilter(formData);
        });

        // Prevent form from closing when clicking inside
        advancedFilterForm.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }
}

// Handle Advanced Filter
function handleAdvancedFilter(formData) {
    let filteredTransactions = [...transactions];

    const amount = parseFloat(formData.get('amount'));
    const dateFrom = formData.get('dateFrom');
    const dateTo = formData.get('dateTo');
    const filterType = formData.get('filterType');

    // Amount filtering
    if (!isNaN(amount)) {
        switch (filterType) {
            case 'over':
                filteredTransactions = filteredTransactions.filter(t => 
                    parseFloat(t.amount.replace(/[^0-9.-]+/g, '')) > amount
                );
                break;
            case 'below':
                filteredTransactions = filteredTransactions.filter(t => 
                    parseFloat(t.amount.replace(/[^0-9.-]+/g, '')) < amount
                );
                break;
        }
    }

    // Date filtering
    if (dateFrom) {
        const fromDate = new Date(dateFrom);
        filteredTransactions = filteredTransactions.filter(t => 
            new Date(t.date) >= fromDate
        );
    }

    if (dateTo) {
        const toDate = new Date(dateTo);
        toDate.setHours(23, 59, 59, 999);
        filteredTransactions = filteredTransactions.filter(t => 
            new Date(t.date) <= toDate
        );
    }

    displayTransactions(filteredTransactions);
    document.getElementById('advancedFilterForm').classList.add('hidden');
}

// Apply Current Filters
function applyCurrentFilters() {
    let filteredTransactions = [...transactions];

    switch (currentFilterType) {
        case 'in':
            filteredTransactions = filteredTransactions.filter(t => t.type === "Received");
            break;
        case 'out':
            filteredTransactions = filteredTransactions.filter(t => t.type === "Sent");
            break;
    }

    displayTransactions(filteredTransactions);
}

// Display Transactions
function displayTransactions(filteredTransactions = transactions) {
    const tbody = document.getElementById("transactionsTableBody");
    if (!tbody) return;

    tbody.innerHTML = filteredTransactions.map(transaction => `
        <tr class="hover:bg-gray-50 transition-colors duration-200">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                ${transaction.date}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    transaction.type === "Received" 
                        ? "bg-green-100 text-green-800" 
                        : "bg-red-100 text-red-800"
                }">
                    ${transaction.type}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                ${transaction.wallet}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-right font-medium ${
                transaction.type === "Received" 
                    ? "text-green-600" 
                    : "text-red-600"
            }">
                ${transaction.amount}
            </td>
        </tr>
    `).join('');

    // Empty state
    if (filteredTransactions.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="4" class="px-6 py-8 text-center text-gray-500">
                    No transactions found matching your filters
                </td>
            </tr>
        `;
    }
}

// Reset Filters
function resetFilters() {
    const advancedFilterForm = document.getElementById('advancedFilterForm');
    if (advancedFilterForm) {
        advancedFilterForm.reset();
    }
    currentFilterType = 'all';
    updateFilterButtons('filterAll');
}

// Initialize Application
function initializeApp() {
    try {
        // Check for required elements
        const requiredElements = ['mainNav', 'transactionsTableBody'];
        for (const elementId of requiredElements) {
            if (!document.getElementById(elementId)) {
                throw new Error(`Required element #${elementId} not found`);
            }
        }

        // Initialize components
        initializeNavigation();
        initializeFilterSystem();
        fetchTransactions();

        // Responsive adjustments
        window.addEventListener('resize', () => {
            const advancedFilterForm = document.getElementById('advancedFilterForm');
            if (window.innerWidth < 768 && advancedFilterForm) {
                advancedFilterForm.classList.add('hidden');
            }
        });

    } catch (error) {
        console.error('Failed to initialize application:', error);
    }
}

// Start the application when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeApp);