/**
 * Authentication related functions
 */

/**
 * Handle user login
 * @param {Event} event - Form submit event
 * @returns {boolean} false to prevent form submission
 */
async function login(event) {
    event.preventDefault();
    
    const form = event.target;
    const email = sanitizeInput(form.email.value);
    const password = form.password.value;
    
    try {
        const response = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Login failed');
        }
        
        // Store authentication data
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('userInfo', JSON.stringify(data.user_info));
        
        // Redirect based on role
        if (data.user_info.role === 'admin') {
            window.location.href = '/admin/dashboard.html';
        } else {
            window.location.href = '/dashboard.html';
        }
        
    } catch (error) {
        showError(error.message);
    }
    
    return false;
}

/**
 * Handle user registration
 * @param {Event} event - Form submit event
 * @returns {boolean} false to prevent form submission
 */
async function register(event) {
    event.preventDefault();
    
    const form = event.target;
    const name = sanitizeInput(form.name.value);
    const email = sanitizeInput(form.email.value);
    const password = form.password.value;
    const confirmPassword = form.confirmPassword.value;
    
    if (password !== confirmPassword) {
        showError('Passwords do not match');
        return false;
    }
    
    try {
        const response = await fetch('/api/v1/auth/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name,
                email,
                password
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Registration failed');
        }
        
        // Redirect to login page
        window.location.href = '/login.html?registered=true';
        
    } catch (error) {
        showError(error.message);
    }
    
    return false;
}

/**
 * Handle password reset request
 * @param {Event} event - Form submit event
 * @returns {boolean} false to prevent form submission
 */
async function requestPasswordReset(event) {
    event.preventDefault();
    
    const form = event.target;
    const email = sanitizeInput(form.email.value);
    
    try {
        const response = await fetch('/api/v1/auth/forgot-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Failed to request password reset');
        }
        
        // Show success message
        showMessage('Password reset instructions have been sent to your email');
        
    } catch (error) {
        showError(error.message);
    }
    
    return false;
}

/**
 * Handle password reset
 * @param {Event} event - Form submit event
 * @returns {boolean} false to prevent form submission
 */
async function resetPassword(event) {
    event.preventDefault();
    
    const form = event.target;
    const token = new URLSearchParams(window.location.search).get('token');
    const password = form.password.value;
    const confirmPassword = form.confirmPassword.value;
    
    if (password !== confirmPassword) {
        showError('Passwords do not match');
        return false;
    }
    
    try {
        const response = await fetch('/api/v1/auth/reset-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token,
                password
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Failed to reset password');
        }
        
        // Redirect to login page
        window.location.href = '/login.html?reset=true';
        
    } catch (error) {
        showError(error.message);
    }
    
    return false;
}

/**
 * Handle user logout
 */
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('userInfo');
    window.location.href = '/login.html';
}

/**
 * Setup authentication-related event handlers
 */
document.addEventListener('DOMContentLoaded', function() {
    // Add password strength indicator
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            const strength = checkPasswordStrength(this.value);
            const indicator = document.getElementById('passwordStrength');
            if (indicator) {
                indicator.style.width = (strength.score * 20) + '%';
                indicator.style.backgroundColor = getStrengthColor(strength.score);
                indicator.title = strength.feedback;
            }
        });
    }
});

/**
 * Get color for password strength indicator
 * @param {number} score - Password strength score
 * @returns {string} Color code
 */
function getStrengthColor(score) {
    const colors = {
        0: '#e74c3c',  // Very weak
        1: '#e67e22',  // Weak
        2: '#f1c40f',  // Moderate
        3: '#2ecc71',  // Strong
        4: '#27ae60'   // Very strong
    };
    return colors[score] || colors[0];
}
