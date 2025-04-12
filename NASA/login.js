const backendUrl = 'http://127.0.0.1:8000'; // Backend URL
const form = document.getElementById('authForm');
const formTitle = document.getElementById('formTitle');
const toggleAuth = document.getElementById('toggleAuth');
const submitButton = document.getElementById('submitButton');
const errorMessage = document.getElementById('errorMessage');
const successMessage = document.getElementById('successMessage');
let isLogin = true;

// Toggle between login and registration
toggleAuth.addEventListener('click', (e) => {
    e.preventDefault();
    isLogin = !isLogin;

    // Update UI
    formTitle.textContent = isLogin ? 'Sign in to your account' : 'Create new account';
    submitButton.textContent = isLogin ? 'Sign in' : 'Register';
    toggleAuth.textContent = isLogin ? 'Sign up' : 'Sign in';
    toggleAuth.previousSibling.textContent = isLogin ? 'No account? ' : 'Already have an account? ';

    // Clear messages and form
    errorMessage.style.display = 'none';
    successMessage.style.display = 'none';
    form.reset();
});

// Handle form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Get form data
    const officeName = document.getElementById('officeName').value;
    const password = document.getElementById('password').value;

    // Clear messages
    errorMessage.style.display = 'none';
    successMessage.style.display = 'none';
 
    // Disable submit button
    submitButton.disabled = true;
    submitButton.textContent = 'Processing...';

    try { 
        const endpoint = isLogin ? '/token' : '/register';
        const response = await fetch(`${backendUrl}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                office_name: officeName,
                password: password
            })
        });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Authentication failed');
        }

        if (isLogin) {
            // Store tokens and user data
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
            localStorage.setItem('office_name', data.office_name);
            localStorage.setItem('wallet_address', data.wallet_address);
            
            // Redirect to home.html after successful login
            window.location.href = 'index.html';
        } else {
            // Show success message and switch to login
            successMessage.textContent = 'Registration successful! Please sign in.';
            successMessage.style.display = 'block';

            // Switch to login form after successful registration
            setTimeout(() => {
                toggleAuth.click();
            }, 2000);
        }
        form.reset();
    } catch (err) {
        errorMessage.textContent = err.message;
        errorMessage.style.display = 'block';
    } finally {
        // Re-enable submit button
        submitButton.disabled = false;
        submitButton.textContent = isLogin ? 'Sign in' : 'Register';
    }
});

// Utility function for token refresh
async function refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');

    try {
        const response = await fetch(`${backendUrl}/refresh-token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                refresh_token: refreshToken
            })
        });
        const data = await response.json();

        if (!response.ok) throw new Error('Token refresh failed');

        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);

        return data.access_token;
    } catch (error) {
        // Handle refresh failure
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('office_name');
        localStorage.removeItem('wallet_address');
        // Update login redirect path
        window.location.href = '/NASA/login.html';
        throw error;
    }
}