// // Device Data Manager JavaScript
// // Handles real-time device data display and charts

// class DeviceDataManager {
//     constructor() {
//         this.temperatureChart = null;
//         this.humidityChart = null;
//         this.refreshInterval = null;
//         this.isLoading = false;
        
//         this.init();
//     }

//     init() {
//         console.log('Initializing Device Data Manager...');
//         this.setupCharts();
//         this.loadDeviceData();
//         this.loadDeviceStats();
//         this.startAutoRefresh();
        
//         // Add event listeners
//         document.addEventListener('DOMContentLoaded', () => {
//             this.bindEvents();
//         });
//     }

//     bindEvents() {
//         // Add refresh button event if it exists
//         const refreshBtn = document.querySelector('[onclick="refreshDeviceData()"]');
//         if (refreshBtn) {
//             refreshBtn.onclick = () => this.refreshDeviceData();
//         }
//     }

//     showSpinner() {
//         const spinner = document.querySelector('.spinner-container');
//         if (spinner) {
//             spinner.style.display = 'block';
//         }
//         this.isLoading = true;
//     }

//     hideSpinner() {
//         const spinner = document.querySelector('.spinner-container');
//         if (spinner) {
//             spinner.style.display = 'none';
//         }
//         this.isLoading = false;
//     }

//     async loadDeviceData() {
//         if (this.isLoading) return;
        
//         try {
//             this.showSpinner();
//             console.log('Loading device data...');
            
//             const response = await fetch('/api/device-data', {
//                 method: 'GET',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 credentials: 'include'
//             });

//             if (!response.ok) {
//                 throw new Error(`HTTP error! status: ${response.status}`);
//             }

//             const result = await response.json();
//             console.log('Device data loaded:', result);

//             if (result.success && result.data) {
//                 this.displayDeviceData(result.data);
//                 this.updateCharts(result.data);
//             } else {
//                 console.error('Failed to load device data:', result);
//                 this.showError('Failed to load device data');
//             }

//         } catch (error) {
//             console.error('Error loading device data:', error);
//             this.showError('Error loading device data: ' + error.message);
//         } finally {
//             this.hideSpinner();
//         }
//     }

//     async loadDeviceStats() {
//         try {
//             console.log('Loading device statistics...');
            
//             const response = await fetch('/api/device-data/stats', {
//                 method: 'GET',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 credentials: 'include'
//             });

//             if (!response.ok) {
//                 throw new Error(`HTTP error! status: ${response.status}`);
//             }

//             const result = await response.json();
//             console.log('Device stats loaded:', result);

//             if (result.success && result.stats) {
//                 this.updateStatistics(result.stats);
//             }

//         } catch (error) {
//             console.error('Error loading device stats:', error);
//         }
//     }

//     displayDeviceData(devices) {
//         const tableBody = document.querySelector('#deviceDataTable tbody');
//         if (!tableBody) {
//             console.error('Device data table not found');
//             return;
//         }

//         // Clear existing data
//         tableBody.innerHTML = '';

//         if (!devices || devices.length === 0) {
//             tableBody.innerHTML = `
//                 <tr>
//                     <td colspan="6" class="text-center text-muted">
//                         <i class="bi bi-inbox"></i> No device data available
//                         <br><small>Device data will appear here once devices start reporting</small>
//                     </td>
//                 </tr>
//             `;
//             return;
//         }

//         // Add device data rows
//         devices.forEach(device => {
//             const row = this.createDeviceRow(device);
//             tableBody.appendChild(row);
//         });

//         console.log(`Displayed ${devices.length} device records`);
//     }

//     createDeviceRow(device) {
//         const row = document.createElement('tr');
        
//         // Format timestamp
//         const timestamp = new Date(device.timestamp).toLocaleString();
        
//         // Determine status badge
//         const statusBadge = device.is_active 
//             ? '<span class="badge bg-success">Active</span>'
//             : '<span class="badge bg-secondary">Inactive</span>';
        
//         // Battery level color
//         const batteryClass = device.battery_level < 20 ? 'text-danger' : 
//                            device.battery_level < 50 ? 'text-warning' : 'text-success';
        
//         // Temperature color
//         const tempClass = device.temperature > 30 ? 'text-danger' : 
//                          device.temperature > 25 ? 'text-warning' : 'text-info';

//         row.innerHTML = `
//             <td><strong>${device.device_id}</strong></td>
//             <td class="${tempClass}">${device.temperature}°C</td>
//             <td class="text-primary">${device.humidity || 0}%</td>
//             <td class="${batteryClass}">
//                 ${device.battery_level}%
//                 ${device.battery_level < 20 ? '<i class="bi bi-battery-half text-danger ms-1"></i>' : ''}
//             </td>
//             <td><small>${timestamp}</small></td>
//             <td>${statusBadge}</td>
//         `;

//         return row;
//     }

//     updateStatistics(stats) {
//         // Update stat cards
//         const statElements = {
//             'totalDevices': stats.total_devices || 0,
//             'activeDevices': stats.active_devices || 0,
//             'deviceWarnings': stats.low_battery_warnings || 0,
//             'criticalAlerts': stats.high_temp_alerts || 0
//         };

//         Object.entries(statElements).forEach(([elementId, value]) => {
//             const element = document.getElementById(elementId);
//             if (element) {
//                 // Animate the number change
//                 this.animateNumber(element, parseInt(element.textContent) || 0, value);
//             }
//         });

//         console.log('Statistics updated:', stats);
//     }

//     animateNumber(element, start, end) {
//         const duration = 1000; // 1 second
//         const range = end - start;
//         const increment = range / (duration / 16); // 60 FPS
//         let current = start;

//         const timer = setInterval(() => {
//             current += increment;
//             if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
//                 current = end;
//                 clearInterval(timer);
//             }
//             element.textContent = Math.round(current);
//         }, 16);
//     }

//     setupCharts() {
//         const tempCtx = document.getElementById('temperatureChart');
//         const humidityCtx = document.getElementById('humidityChart');

//         if (!tempCtx || !humidityCtx) {
//             console.warn('Chart canvases not found');
//             return;
//         }

//         // Temperature Chart
//         this.temperatureChart = new Chart(tempCtx, {
//             type: 'line',
//             data: {
//                 labels: [],
//                 datasets: [{
//                     label: 'Temperature (°C)',
//                     data: [],
//                     borderColor: 'rgb(255, 99, 132)',
//                     backgroundColor: 'rgba(255, 99, 132, 0.1)',
//                     borderWidth: 2,
//                     fill: true,
//                     tension: 0.4
//                 }]
//             },
//             options: {
//                 responsive: true,
//                 maintainAspectRatio: false,
//                 plugins: {
//                     legend: {
//                         display: true,
//                         position: 'top'
//                     }
//                 },
//                 scales: {
//                     y: {
//                         beginAtZero: true,
//                         title: {
//                             display: true,
//                             text: 'Temperature (°C)'
//                         }
//                     },
//                     x: {
//                         title: {
//                             display: true,
//                             text: 'Time'
//                         }
//                     }
//                 }
//             }
//         });

//         // Humidity Chart
//         this.humidityChart = new Chart(humidityCtx, {
//             type: 'line',
//             data: {
//                 labels: [],
//                 datasets: [{
//                     label: 'Humidity (%)',
//                     data: [],
//                     borderColor: 'rgb(54, 162, 235)',
//                     backgroundColor: 'rgba(54, 162, 235, 0.1)',
//                     borderWidth: 2,
//                     fill: true,
//                     tension: 0.4
//                 }]
//             },
//             options: {
//                 responsive: true,
//                 maintainAspectRatio: false,
//                 plugins: {
//                     legend: {
//                         display: true,
//                         position: 'top'
//                     }
//                 },
//                 scales: {
//                     y: {
//                         beginAtZero: true,
//                         max: 100,
//                         title: {
//                             display: true,
//                             text: 'Humidity (%)'
//                         }
//                     },
//                     x: {
//                         title: {
//                             display: true,
//                             text: 'Time'
//                         }
//                     }
//                 }
//             }
//         });

//         console.log('Charts initialized');
//     }

//     async updateCharts(devices) {
//         if (!this.temperatureChart || !this.humidityChart) {
//             console.warn('Charts not initialized');
//             return;
//         }

//         try {
//             const response = await fetch('/api/device-data/chart', {
//                 method: 'GET',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 credentials: 'include'
//             });

//             if (response.ok) {
//                 const result = await response.json();
//                 if (result.success && result.chart_data) {
//                     const { labels, temperature, humidity } = result.chart_data;

//                     // Update temperature chart
//                     this.temperatureChart.data.labels = labels;
//                     this.temperatureChart.data.datasets[0].data = temperature;
//                     this.temperatureChart.update('none');

//                     // Update humidity chart
//                     this.humidityChart.data.labels = labels;
//                     this.humidityChart.data.datasets[0].data = humidity;
//                     this.humidityChart.update('none');
//                 }
//             }
//         } catch (error) {
//             console.error('Error updating charts:', error);
//         }
//     }

//     startAutoRefresh() {
//         // Refresh every 30 seconds
//         this.refreshInterval = setInterval(() => {
//             console.log('Auto-refreshing device data...');
//             this.loadDeviceData();
//             this.loadDeviceStats();
//         }, 30000);

//         console.log('Auto-refresh started (30 seconds interval)');
//     }

//     stopAutoRefresh() {
//         if (this.refreshInterval) {
//             clearInterval(this.refreshInterval);
//             this.refreshInterval = null;
//             console.log('Auto-refresh stopped');
//         }
//     }

//     async refreshDeviceData() {
//         console.log('Manual refresh triggered');
//         await this.loadDeviceData();
//         await this.loadDeviceStats();
        
//         // Show success message
//         this.showSuccess('Device data refreshed successfully');
//     }

//     showError(message) {
//         console.error(message);
//         // You can implement a toast notification system here
//         alert('Error: ' + message);
//     }

//     showSuccess(message) {
//         console.log(message);
//         // You can implement a toast notification system here
//         // For now, just log to console
//     }

//     // Simulate device data for testing
//     async simulateDeviceData() {
//         try {
//             const response = await fetch('/api/device-data/simulate', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 credentials: 'include'
//             });

//             if (response.ok) {
//                 const result = await response.json();
//                 console.log('Simulated device data:', result);
//                 this.showSuccess('Device data simulated successfully');
                
//                 // Refresh data after simulation
//                 setTimeout(() => {
//                     this.refreshDeviceData();
//                 }, 1000);
//             }
//         } catch (error) {
//             console.error('Error simulating device data:', error);
//             this.showError('Failed to simulate device data');
//         }
//     }
// }

// // Device Data Management Functions

// // Initialize tooltips and device count
// document.addEventListener('DOMContentLoaded', function() {
//     var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
//     var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
//         return new bootstrap.Tooltip(tooltipTriggerEl)
//     });

//     // Initialize device count
//     updateDeviceCount();

//     // Setup search functionality
//     setupSearchFunctionality();
// });

// // Mobile sidebar toggle
// document.querySelector('.navbar-toggler')?.addEventListener('click', () => {
//     document.getElementById('sidebar').classList.toggle('show');
// });

// // Table search functionality
// function setupSearchFunctionality() {
//     document.getElementById('deviceSearch')?.addEventListener('input', (e) => {
//         const searchTerm = e.target.value.toLowerCase();
//         const rows = document.querySelectorAll('#staticDeviceTable tbody tr');
//         rows.forEach(row => {
//             const text = row.textContent.toLowerCase();
//             row.style.display = text.includes(searchTerm) ? '' : 'none';
//         });
//         updateDeviceCount();
//     });
// }

// // Update device count
// function updateDeviceCount() {
//     const visibleRows = document.querySelectorAll('#staticDeviceTable tbody tr:not([style*="display: none"])');
//     const count = document.getElementById('deviceCount');
//     if (count) {
//         count.textContent = visibleRows.length;
//     }
// }

// // View device details
// function viewDeviceDetails(deviceId) {
//     // Show loading spinner
//     const spinner = document.getElementById('spinner');
//     if (spinner) spinner.style.display = 'block';

//     // Get device details via API
//     fetch(`/api/devices/${deviceId}`)
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         })
//         .then(device => {
//             // Populate modal fields
//             document.getElementById('modalDeviceId').textContent = device.Device_ID;
//             document.getElementById('modalBatteryLevel').textContent = device.Battery_Level;
//             document.getElementById('modalTemperature').textContent = device.First_Sensor_temperature;
//             document.getElementById('modalRouteFrom').textContent = device.Route_From;
//             document.getElementById('modalRouteTo').textContent = device.Route_To;
//             document.getElementById('modalLastUpdated').textContent = 
//                 device.Last_Updated ? new Date(device.Last_Updated).toLocaleString() : 'N/A';

//             // Show modal
//             const modal = new bootstrap.Modal(document.getElementById('deviceDetailsModal'));
//             modal.show();
//         })
//         .catch(error => {
//             console.error('Error fetching device details:', error);
//             alert('Failed to load device details. Please try again.');
//         })
//         .finally(() => {
//             // Hide loading spinner
//             if (spinner) spinner.style.display = 'none';
//         });
// }

// // Edit device
// function editDevice(deviceId) {
//     window.location.href = `/devices/${deviceId}/edit`;
// }

// // Delete device
// function deleteDevice(deviceId) {
//     if (confirm('Are you sure you want to delete this device? This action cannot be undone.')) {
//         // Show loading spinner
//         const spinner = document.getElementById('spinner');
//         if (spinner) spinner.style.display = 'block';

//         fetch(`/api/devices/${deviceId}`, {
//             method: 'DELETE',
//             headers: {
//                 'Content-Type': 'application/json'
//             }
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         })
//         .then(() => {
//             // Remove the row from the table
//             const row = document.querySelector(`tr[data-device-id="${deviceId}"]`);
//             if (row) {
//                 row.remove();
//                 updateDeviceCount();
//             }
//             alert('Device deleted successfully');
//         })
//         .catch(error => {
//             console.error('Error deleting device:', error);
//             alert('Failed to delete device. Please try again.');
//         })
//         .finally(() => {
//             // Hide loading spinner
//             if (spinner) spinner.style.display = 'none';
//         });
//     }
// }

// // Refresh device data
// function refreshDeviceData() {
//     window.location.reload();
// }

// // Global functions for backward compatibility
// function refreshDeviceData() {
//     if (window.deviceDataManager) {
//         window.deviceDataManager.refreshDeviceData();
//     }
// }

// function simulateDeviceData() {
//     if (window.deviceDataManager) {
//         window.deviceDataManager.simulateDeviceData();
//     }
// }

// // Initialize when DOM is loaded
// document.addEventListener('DOMContentLoaded', function() {
//     console.log('DOM loaded, initializing Device Data Manager...');
//     window.deviceDataManager = new DeviceDataManager();
// });

// // Cleanup on page unload
// window.addEventListener('beforeunload', function() {
//     if (window.deviceDataManager) {
//         window.deviceDataManager.stopAutoRefresh();
//     }
// });