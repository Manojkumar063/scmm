// // Handle login form submission
// document.getElementById('loginForm').addEventListener('submit', async function(e) {
//     e.preventDefault();
    
//     // Get form elements
//     const emailInput = document.getElementById('email');  // Changed from username to email
//     const passwordInput = document.getElementById('password');
//     const errorElement = document.getElementById('errorMessage');
//     const submitButton = this.querySelector('button[type="submit"]');
    
//     // Clear previous errors
//     errorElement.textContent = '';
//     errorElement.classList.add('d-none');
    
//     // Get values
//     const email = emailInput.value.trim();
//     const password = passwordInput.value;
    
//     // Client-side validation
//     if (!email) {
//         showError(errorElement, 'Email is required');
//         emailInput.focus();
//         return;
//     }
    
//     if (!password) {
//         showError(errorElement, 'Password is required');
//         passwordInput.focus();
//         return;
//     }

//     // Basic email format validation
//     if (!validateEmail(email)) {
//         showError(errorElement, 'Please enter a valid email address');
//         emailInput.focus();
//         return;
//     }

//     try {
//         // Disable button during request
//         submitButton.disabled = true;
//         submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Logging in...';
        
//         const response = await fetch('/login', {  // Changed from /auth/login to match your backend
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/x-www-form-urlencoded',
//             },
//             body: new URLSearchParams({
//                 email: email,
//                 password: password
//             })
//         });

//         if (response.redirected) {
//             // Successful login - follow the redirect
//             window.location.href = response.url;
//             return;
//         }

//         // Handle non-redirect responses (errors)
//         const contentType = response.headers.get('content-type');
//         if (contentType && contentType.includes('application/json')) {
//             const data = await response.json();
//             showError(errorElement, data.message || 'Login failed');
//         } else {
//             const text = await response.text();
//             showError(errorElement, text || 'Login failed');
//         }
//     } catch (error) {
//         console.error('Login error:', error);
//         showError(errorElement, 'An error occurred during login. Please try again.');
//     } finally {
//         // Re-enable button
//         submitButton.disabled = false;
//         submitButton.textContent = 'Login';
//     }
// });

// function showError(element, message) {
//     element.textContent = message;
//     element.classList.remove('d-none');
//     // Optional: Scroll to error message
//     element.scrollIntoView({ behavior: 'smooth', block: 'center' });
// }

// function validateEmail(email) {
//     const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
//     return re.test(String(email).toLowerCase());
// }