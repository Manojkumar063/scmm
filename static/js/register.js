// document.addEventListener('DOMContentLoaded', () => {
//     const registerForm = document.getElementById('registerForm');
//     const submitButton = registerForm.querySelector('button[type="submit"]');
//     const loadingSpinner = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Loading...';

//     registerForm.addEventListener('submit', async function(e) {
//         e.preventDefault();
        
//         // Disable submit button and show loading state
//         submitButton.disabled = true;
//         const originalText = submitButton.innerHTML;
//         submitButton.innerHTML = loadingSpinner;

//         const formData = new FormData(this);

//         try {
//             const response = await fetch('/register', {
//                 method: 'POST',
//                 body: formData,
//                 headers: {
//                     'Accept': 'application/json'
//                 },
//                 redirect: 'manual'
//             });

//             console.log("Response status:", response.status);
    
//     // Handle redirect manually
//     if (response.status === 303 || response.status === 302) {
//         console.log("Redirecting to:", response.headers.get('Location'));
//         window.location.href = response.headers.get('Location') || '/login';
//         return;
//     }
    
//     // Try to parse as JSON first, then fallback to text
//     let data;
//     try {
//         data = await response.json();
//     } catch (e) {
//         data = await response.text();
//     }
    
//     // If we got HTML back (template response)
//     if (typeof data === 'string' && data.includes('<html')) {
//         const parser = new DOMParser();
//         const doc = parser.parseFromString(data, 'text/html');
//         const alert = doc.querySelector('.alert');
//         if (alert) {
//             throw new Error(alert.textContent.trim());
//         }
//         throw new Error("Registration failed (unknown error)");
//     }
    
//     // If we got JSON back
//     if (data && data.message) {
//         throw new Error(data.message);
//     }
    
//     // If we got here, it's an unknown response
//     throw new Error("Unexpected response from server");
// })
// .catch(error => {
//     console.error("Registration error:", error);
//     showError(error.message || "Regoog. Please try again.");
// })
// .finally(() => {
//     submitButton.textContent = originalText;
//     submitButton.disabled = false;
// });