// API Configuration - can be overridden by config.js
const API_URL = window.CONFIG?.API_URL || window.location.origin + '/api';

function showRegister() {
    document.getElementById('loginForm').classList.remove('active');
    document.getElementById('registerForm').classList.add('active');
    hideMessage();
}

function showLogin() {
    document.getElementById('registerForm').classList.remove('active');
    document.getElementById('loginForm').classList.add('active');
    hideMessage();
}

function showMessage(text, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = text;
    messageDiv.className = `message ${type} show`;
    
    setTimeout(() => {
        hideMessage();
    }, 5000);
}

function hideMessage() {
    const messageDiv = document.getElementById('message');
    messageDiv.classList.remove('show');
}

async function handleLogin(event) {
    event.preventDefault();
    
    const emailOrUsername = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    // Determine if input is email or username
    const isEmail = emailOrUsername.includes('@');
    
    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                email: isEmail ? emailOrUsername : undefined,
                username: !isEmail ? emailOrUsername : undefined,
                password 
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Store JWT token in localStorage
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            
            showMessage('Login successful! Redirecting...', 'success');
            setTimeout(() => {
                window.location.href = '/';
            }, 500);
        } else {
            showMessage(data.error || 'Login failed', 'error');
        }
    } catch (error) {
        showMessage('Connection error. Please try again.', 'error');
        console.error('Login error:', error);
    }
}

async function handleRegister(event) {
    event.preventDefault();
    
    const organizationId = document.getElementById('regOrgId').value;
    const fullName = document.getElementById('regFullName').value;
    const username = document.getElementById('regUsername').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    const confirmPassword = document.getElementById('regConfirmPassword').value;
    
    // Validate passwords match
    if (password !== confirmPassword) {
        showMessage('Passwords do not match!', 'error');
        return;
    }
    
    // Validate password length
    if (password.length < 6) {
        showMessage('Password must be at least 6 characters long!', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                organization_id: parseInt(organizationId),
                full_name: fullName,
                username,
                email,
                password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage('Registration successful! Please login.', 'success');
            setTimeout(() => {
                showLogin();
                document.getElementById('loginEmail').value = email;
            }, 1500);
        } else {
            showMessage(data.error || 'Registration failed', 'error');
        }
    } catch (error) {
        showMessage('Connection error. Please try again.', 'error');
        console.error('Registration error:', error);
    }
}

// Check if already logged in
window.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    if (token) {
        try {
            const response = await fetch(`${API_URL}/check-auth`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (response.ok) {
                window.location.href = '/dashboard';
            } else {
                // Token invalid, clear it
                localStorage.removeItem('token');
                localStorage.removeItem('user');
            }
        } catch (error) {
            console.log('Not logged in');
        }
    }
});
