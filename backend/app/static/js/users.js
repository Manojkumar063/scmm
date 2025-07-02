// <!-- JavaScript Dependencies -->
// <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>

// <!-- Inline JavaScript for Interactivity -->
// <script>
//     // Toggle Sidebar for Mobile View
//     function toggleSidebar() {
//         document.querySelector('.sidebar').classList.toggle('show');
//     }

//     // Show Loading Spinner
//     function showSpinner() {
//         document.getElementById('spinner').style.display = 'flex';
//     }

//     // Hide Loading Spinner
//     function hideSpinner() {
//         document.getElementById('spinner').style.display = 'none';
//     }

//     // Display Alert Messages
//     function showAlert(message, type = 'success') {
//         const alertContainer = document.getElementById('alertContainer');
//         const alert = document.createElement('div');
//         alert.className = `alert alert-${type} alert-dismissible fade show`;
//         alert.innerHTML = `
//             <i class="bi bi-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2"></i>
//             ${message}
//             <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
//         `;
//         alertContainer.appendChild(alert);
//         setTimeout(() => {
//             const bsAlert = new bootstrap.Alert(alert);
//             bsAlert.close();
//         }, 3000);
//     }

//     // Fetch User Details for Edit Modal
//     async function editUser(email) {
//         try {
//             showSpinner();
//             const response = await fetch(`/api/users/${email}`, {
//                 method: 'GET',
//                 headers: {
//                     'Content-Type': 'application/json'
//                 }
//             });
//             const user = await response.json();

//             if (!response.ok) {
//                 throw new Error(user.detail || 'Failed to fetch user details');
//             }

//             document.getElementById('editUserEmail').value = user.email;
//             document.getElementById('editUsername').value = user.username;
//             document.getElementById('editEmail').value = user.email;
//             document.getElementById('editRole').value = user.role;
//             document.getElementById('editStatus').value = user.status || 'active';

//             const modal = new bootstrap.Modal(document.getElementById('editUserModal'));
//             modal.show();
//         } catch (error) {
//             showAlert(error.message, 'danger');
//         } finally {
//             hideSpinner();
//         }
//     }

//     // Save User Changes
//     async function saveUserChanges() {
//         const email = document.getElementById('editUserEmail').value;
//         const username = document.getElementById('editUsername').value;
//         const role = document.getElementById('editRole').value;
//         const status = document.getElementById('editStatus').value;

//         try {
//             showSpinner();
//             const response = await fetch(`/api/users/${email}`, {
//                 method: 'PUT',
//                 headers: {
//                     'Content-Type': 'application/json'
//                 },
//                 body: JSON.stringify({ username, role, status })
//             });
//             const result = await response.json();

//             if (!response.ok) {
//                 throw new Error(result.detail || 'Failed to update user');
//             }

//             showAlert('User updated successfully', 'success');
//             const modal = bootstrap.Modal.getInstance(document.getElementById('editUserModal'));
//             modal.hide();
//             refreshUsers();
//         } catch (error) {
//             showAlert(error.message, 'danger');
//         } finally {
//             hideSpinner();
//         }
//     }

//     // Delete User
//     async function deleteUser(email) {
//         if (!confirm(`Are you sure you want to delete the user with email ${email}?`)) {
//             return;
//         }

//         try {
//             showSpinner();
//             const response = await fetch(`/api/users/${email}`, {
//                 method: 'DELETE',
//                 headers: {
//                     'Content-Type': 'application/json'
//                 }
//             });
//             const result = await response.json();

//             if (!response.ok) {
//                 throw new Error(result.detail || 'Failed to delete user');
//             }

//             showAlert('User deleted successfully', 'success');
//             refreshUsers();
//         } catch (error) {
//             showAlert(error.message, 'danger');
//         } finally {
//             hideSpinner();
//         }
//     }

//     // Refresh User List
//     async function refreshUsers() {
//         try {
//             showSpinner();
//             const response = await fetch('/users', {
//                 method: 'GET',
//                 headers: {
//                     'Content-Type': 'application/json'
//                 }
//             });
//             if (!response.ok) {
//                 throw new Error('Failed to refresh user list');
//             }
//             window.location.reload();
//         } catch (error) {
//             showAlert(error.message, 'danger');
//         } finally {
//             hideSpinner();
//         }
//     }
// </script>
