// // Form validation
// function validateForm(form) {
//     const inputs = form.querySelectorAll('input, textarea');
//     let isValid = true;

//     inputs.forEach(input => {
//         if (!input.checkValidity()) {
//             input.classList.add('is-invalid');
//             isValid = false;
//         } else {
//             input.classList.remove('is-invalid');
//             input.classList.add('is-valid');
//         }
//     });

//     return isValid;
// }

// // Show error in toast
// function showError(message) {
//     const errorToast = document.getElementById('errorToast');
//     const errorMessage = document.getElementById('errorMessage');
//     errorMessage.textContent = message;
//     const toast = new bootstrap.Toast(errorToast);
//     toast.show();
// }

// // Show loading spinner
// function toggleLoading(show) {
//     const spinner = document.querySelector('.spinner-container');
//     spinner.style.display = show ? 'flex' : 'none';
// }

// // Handle form submission
// async function handleShipmentCreate(event) {
//     event.preventDefault();
    
//     const form = event.target;
    
//     // Validate form
//     if (!validateForm(form)) {
//         return false;
//     }
    
//     toggleLoading(true);
    
//     try {
//         const formData = {
//             shipment_number: sanitizeInput(form.shipmentNumber.value),
//             route: sanitizeInput(form.routeDetails.value), // Changed from route_details
//             device_id: sanitizeInput(form.deviceId.value),
//             po_number: sanitizeInput(form.poNumber.value),
//             ndc_number: sanitizeInput(form.ndcNumber.value),
//             goods_number: sanitizeInput(form.serialNumberOfGoods.value), // Changed from serial_number_of_goods
//             container_number: sanitizeInput(form.containerNumber.value),
//             goods_type: sanitizeInput(form.goodsType.value),
//             expected_delivery_date: form.expectedDeliveryDate.value, // Remove .toISOString() for form data
//             delivery_number: sanitizeInput(form.deliveryNumber.value),
//             batch_id: sanitizeInput(form.batchId.value),
//             shipment_description: sanitizeInput(form.shipmentDescription.value)
//         };

//         // Also change the fetch URL and method
//         const response = await fetch('/new_shipment', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/x-www-form-urlencoded',
//             },
//             body: new URLSearchParams(formData)
//         });
        
//         // Your backend returns HTML templates, not JSON
//         if (!response.ok) {
//             throw new Error('Failed to create shipment');
//         }

//         // Check if creation was successful by looking at the response
//         const responseText = await response.text();
//         if (responseText.includes('Shipment created successfully')) {
//             // Success - redirect or show success message
//             window.location.href = '/shipments?created=true';
//         } else if (responseText.includes('already exists')) {
//             // Handle duplicate error
//             const errorMatch = responseText.match(/The \w+_number '(\d+)' already exists/);
//             const errorMessage = errorMatch ? errorMatch[0] : 'Shipment or delivery number already exists';
//             throw new Error(errorMessage);
//         } else if (responseText.includes('Failed to create shipment')) {
//             throw new Error('Failed to create shipment. Please try again.');
//         } else {
//             throw new Error('An unexpected error occurred');
//         }
        
//     } catch (error) {
//         showError(error.message);
//         return false;
//     } finally {
//         toggleLoading(false);
//     }
// }

// // Initialize form validation and set minimum date
// document.addEventListener('DOMContentLoaded', function() {
//     // Set minimum date for expected delivery to tomorrow
//     const expectedDeliveryInput = document.getElementById('expectedDeliveryDate');
//     const tomorrow = new Date();
//     tomorrow.setDate(tomorrow.getDate() + 1);
//     expectedDeliveryInput.min = tomorrow.toISOString().split('.')[0];

//     // Initialize Bootstrap form validation
//     const forms = document.querySelectorAll('.needs-validation');
//     Array.prototype.slice.call(forms).forEach(function(form) {
//         form.addEventListener('submit', function(event) {
//             if (!form.checkValidity()) {
//                 event.preventDefault();
//                 event.stopPropagation();
//             }
//             form.classList.add('was-validated');
//         }, false);
//     });

//     // Add event listeners for input validation
//     const inputs = document.querySelectorAll('input[pattern], input[required], textarea[required]');
//     inputs.forEach(input => {
//         input.addEventListener('input', () => {
//             input.value = sanitizeInput(input.value);
//             if (input.checkValidity()) {
//                 input.classList.remove('is-invalid');
//                 input.classList.add('is-valid');
//             } else {
//                 input.classList.remove('is-valid');
//                 input.classList.add('is-invalid');
//             }
//         });
//     });
// });