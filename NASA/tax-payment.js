const API_URL = 'http://localhost:8000';
let selectedTaxType = '';

// Handle tax type selection
document.querySelectorAll('.tax-card').forEach(card => {
    card.addEventListener('click', function() {
        // Remove selected class from all cards
        document.querySelectorAll('.tax-card').forEach(c => c.classList.remove('selected'));
        
        // Add selected class to clicked card
        this.classList.add('selected');
        
        // Update tax type input
        selectedTaxType = this.getAttribute('data-tax-type');
        document.getElementById('taxType').value = selectedTaxType;
    });
});

// Update summary when amount changes
document.getElementById('amount').addEventListener('input', function() {
    const amount = parseFloat(this.value) || 0;
    document.getElementById('summaryAmount').textContent = `KES ${amount.toFixed(2)}`;
    document.getElementById('summaryTotal').textContent = `KES ${amount.toFixed(2)}`;
});

// Toggle password visibility
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const icon = document.querySelector('.toggle-password i');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// Show message
function showMessage(message, type) {
    const messageEl = document.getElementById('message');
    messageEl.textContent = message;
    messageEl.className = `message ${type}`;
    messageEl.style.display = 'block';
    
    setTimeout(() => {
        messageEl.style.display = 'none';
    }, 5000);
}

// Reset form
function resetForm() {
    document.getElementById('officeName').value = '';
    document.getElementById('password').value = '';
    document.getElementById('amount').value = '';
    document.getElementById('description').value = '';
    document.getElementById('taxType').value = '';
    document.querySelectorAll('.tax-card').forEach(c => c.classList.remove('selected'));
    selectedTaxType = '';
    document.getElementById('summaryAmount').textContent = 'KES 0.00';
    document.getElementById('summaryTotal').textContent = 'KES 0.00';
}

// Pay tax
async function payTax() {
    const officeName = document.getElementById('officeName').value.trim();
    const password = document.getElementById('password').value;
    const amount = parseFloat(document.getElementById('amount').value);
    const description = document.getElementById('description').value.trim();

    // Validation
    if (!selectedTaxType) {
        showMessage('Please select a tax type', 'error');
        return;
    }

    if (!officeName) {
        showMessage('Please enter your office name', 'error');
        return;
    }

    if (!password) {
        showMessage('Please enter your password', 'error');
        return;
    }

    if (!amount || amount <= 0) {
        showMessage('Please enter a valid amount', 'error');
        return;
    }

    if (!description) {
        showMessage('Please enter a reference or description', 'error');
        return;
    }

    try {
        // First, get Finance Office wallet address
        const financeResponse = await fetch(`${API_URL}/finance-office-wallet`);
        if (!financeResponse.ok) {
            showMessage('Could not retrieve Government Finance Office information', 'error');
            return;
        }
        const financeData = await financeResponse.json();
        const financeWallet = financeData.wallet_address;

        // Authenticate to get token
        const loginData = new URLSearchParams();
        loginData.append('username', officeName);
        loginData.append('password', password);

        const loginResponse = await fetch(`${API_URL}/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: loginData
        });

        if (!loginResponse.ok) {
            showMessage('Invalid office name or password', 'error');
            return;
        }

        const loginResult = await loginResponse.json();
        const token = loginResult.access_token;

        // Process tax payment to Government Finance Office
        const taxPayment = {
            recipient_wallet: financeWallet,
            amount: amount,
            purpose: `TAX PAYMENT: ${selectedTaxType} - ${description}`
        };

        const paymentResponse = await fetch(`${API_URL}/send`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(taxPayment)
        });

        const paymentResult = await paymentResponse.json();

        if (!paymentResponse.ok) {
            showMessage(paymentResult.detail || 'Payment failed', 'error');
            return;
        }

        // Show receipt
        displayReceipt({
            taxType: selectedTaxType,
            officeName: officeName,
            amount: amount,
            description: description,
            transactionHash: paymentResult.transaction_hash,
            timestamp: new Date().toLocaleString(),
            recipientOffice: financeData.office_name
        });

        showMessage('Tax payment successfully sent to Government Finance Office!', 'success');
        
    } catch (error) {
        console.error('Error:', error);
        showMessage('An error occurred while processing payment', 'error');
    }
}

// Display receipt
function displayReceipt(data) {
    const receiptDetails = document.getElementById('receiptDetails');
    receiptDetails.innerHTML = `
        <div class="receipt-row">
            <strong>Receipt Date:</strong>
            <span>${data.timestamp}</span>
        </div>
        <div class="receipt-row">
            <strong>Tax Type:</strong>
            <span>${data.taxType}</span>
        </div>
        <div class="receipt-row">
            <strong>Paid By:</strong>
            <span>${data.officeName}</span>
        </div>
        <div class="receipt-row">
            <strong>Paid To:</strong>
            <span style="color: #1e3c72; font-weight: bold;">${data.recipientOffice || 'Government Finance Office'}</span>
        </div>
        <div class="receipt-row">
            <strong>Reference:</strong>
            <span>${data.description}</span>
        </div>
        <div class="receipt-row">
            <strong>Amount Paid:</strong>
            <span style="color: #28a745; font-weight: bold;">KES ${data.amount.toFixed(2)}</span>
        </div>
        <div class="receipt-row">
            <strong>Transaction Hash:</strong>
            <span style="font-size: 0.85em; word-break: break-all;">${data.transactionHash}</span>
        </div>
        <div class="receipt-row">
            <strong>Status:</strong>
            <span style="color: #28a745;"><i class="fas fa-check-circle"></i> Confirmed & Added to Government Revenue</span>
        </div>
    `;

    document.querySelector('.payment-form').style.display = 'none';
    document.getElementById('receipt').style.display = 'block';
}

// Print receipt
function printReceipt() {
    window.print();
}
