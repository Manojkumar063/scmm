// Security utilities for preventing XSS and other attacks

/**
 * Sanitize user input to prevent XSS attacks
 * @param {HTMLInputElement | string} input - Input element or string to sanitize
 * @returns {string} Sanitized string
 */
function sanitizeInput(input) {
    const value = typeof input === 'string' ? input : input.value;
    return value
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#x27;')
        .replace(/\//g, '&#x2F;');
}

/**
 * Validate input against allowed pattern
 * @param {string} value - Value to validate
 * @param {string} pattern - RegExp pattern to test against
 * @returns {boolean} Whether the input is valid
 */
function validateInput(value, pattern) {
    const regex = new RegExp(pattern);
    return regex.test(value);
}

/**
 * Check password strength
 * @param {string} password - Password to check
 * @returns {{score: number, feedback: string}} Password strength score and feedback
 */
function checkPasswordStrength(password) {
    let score = 0;
    let feedback = [];

    // Length check
    if (password.length < 8) {
        feedback.push('Password should be at least 8 characters long');
    } else {
        score += 2;
    }

    // Complexity checks
    if (/[A-Z]/.test(password)) score += 1;
    if (/[a-z]/.test(password)) score += 1;
    if (/[0-9]/.test(password)) score += 1;
    if (/[^A-Za-z0-9]/.test(password)) score += 1;

    // Provide feedback based on score
    if (score < 2) {
        feedback.push('Very weak password');
    } else if (score < 3) {
        feedback.push('Weak password');
    } else if (score < 4) {
        feedback.push('Moderate password');
    } else if (score < 5) {
        feedback.push('Strong password');
    } else {
        feedback.push('Very strong password');
    }

    return {
        score,
        feedback: feedback.join('. ')
    };
}

/**
 * Show error message in modal
 * @param {string} message - Error message to display
 */
function showError(message) {
    const modal = document.getElementById('errorModal');
    const errorMessage = document.getElementById('errorMessage');
    
    errorMessage.textContent = sanitizeInput(message);
    modal.style.display = 'block';
    
    // Close button functionality
    const closeBtn = modal.querySelector('.close');
    closeBtn.onclick = function() {
        modal.style.display = 'none';
    };
    
    // Click outside modal to close
    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    };
}

/**
 * Check if user is authenticated
 * @returns {boolean} Whether user is authenticated
 */
function isAuthenticated() {
    const token = localStorage.getItem('token');
    if (!token) return false;
    
    try {
        // Check token expiration
        const payload = JSON.parse(atob(token.split('.')[1]));
        if (payload.exp * 1000 < Date.now()) {
            localStorage.removeItem('token');
            localStorage.removeItem('userInfo');
            return false;
        }
        return true;
    } catch (e) {
        localStorage.removeItem('token');
        localStorage.removeItem('userInfo');
        return false;
    }
}

/**
 * Protect routes that require authentication
 */
function protectRoute() {
    if (!isAuthenticated()) {
        window.location.href = '/login.html';
    }
}

/**
 * Get user role
 * @returns {string|null} User role or null if not authenticated
 */
function getUserRole() {
    const userInfo = localStorage.getItem('userInfo');
    if (!userInfo) return null;
    
    try {
        return JSON.parse(userInfo).role;
    } catch (e) {
        return null;
    }
}

/**
 * Check if user has required role
 * @param {string[]} requiredRoles - Array of allowed roles
 * @returns {boolean} Whether user has required role
 */
function checkRole(requiredRoles) {
    const userRole = getUserRole();
    return userRole && requiredRoles.includes(userRole);
}

/**
 * Protect route based on role
 * @param {string[]} requiredRoles - Array of allowed roles
 */
function protectRouteByRole(requiredRoles) {
    if (!checkRole(requiredRoles)) {
        window.location.href = '/unauthorized.html';
    }
}
