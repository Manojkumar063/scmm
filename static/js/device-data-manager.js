// Device data management and visualization
class DeviceDataManager {
    constructor() {
        this.charts = {};
        this.monitoringInterval = null;
        this.initialize();
    }

    initialize() {
        this.setupEventListeners();
        this.initializeCharts();
    }

    setupEventListeners() {
        document.getElementById('startMonitoring')?.addEventListener('click', () => this.startMonitoring());
        document.getElementById('stopMonitoring')?.addEventListener('click', () => this.stopMonitoring());
    }

    initializeCharts() {
        const tempCtx = document.getElementById('temperatureChart')?.getContext('2d');
        const batteryCtx = document.getElementById('batteryChart')?.getContext('2d');

        if (tempCtx) {
            this.charts.temperature = new Chart(tempCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Temperature (°C)',
                        data: [],
                        borderColor: '#e74c3c',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }

        if (batteryCtx) {
            this.charts.battery = new Chart(batteryCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Battery Level (%)',
                        data: [],
                        borderColor: '#2ecc71',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }
    }

    async fetchLatestData(deviceId) {
        try {
            showSpinner();
            const response = await fetch(`/api/v1/devices/data/${deviceId}/latest`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch device data');
            }

            const data = await response.json();
            this.updateDashboard(data);
            hideSpinner();
        } catch (error) {
            hideSpinner();
            showAlert('error', error.message);
        }
    }

    updateDashboard(data) {
        this.updateDeviceInfo(data);
        this.updateCharts(data);
        this.checkAlerts(data);
    }

    updateDeviceInfo(data) {
        const deviceInfo = document.getElementById('deviceInfo');
        if (!deviceInfo) return;

        deviceInfo.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Device ${sanitizeInput(data.device_id)}</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <p><strong>Temperature:</strong> ${data.first_sensor_temp}°C</p>
                            <p><strong>Battery Level:</strong> ${data.battery_level}%</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Route:</strong> ${sanitizeInput(data.route_from)} → ${sanitizeInput(data.route_to)}</p>
                            <p><strong>Last Updated:</strong> ${new Date(data.timestamp).toLocaleString()}</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    updateCharts(data) {
        const timestamp = new Date(data.timestamp).toLocaleTimeString();

        if (this.charts.temperature) {
            this.charts.temperature.data.labels.push(timestamp);
            this.charts.temperature.data.datasets[0].data.push(data.first_sensor_temp);
            if (this.charts.temperature.data.labels.length > 20) {
                this.charts.temperature.data.labels.shift();
                this.charts.temperature.data.datasets[0].data.shift();
            }
            this.charts.temperature.update();
        }

        if (this.charts.battery) {
            this.charts.battery.data.labels.push(timestamp);
            this.charts.battery.data.datasets[0].data.push(data.battery_level);
            if (this.charts.battery.data.labels.length > 20) {
                this.charts.battery.data.labels.shift();
                this.charts.battery.data.datasets[0].data.shift();
            }
            this.charts.battery.update();
        }
    }

    checkAlerts(data) {
        if (data.first_sensor_temp > 30) {
            showAlert('warning', `High temperature alert: ${data.first_sensor_temp}°C`);
        }
        if (data.battery_level < 20) {
            showAlert('warning', `Low battery alert: ${data.battery_level}%`);
        }
    }

    startMonitoring() {
        const deviceId = document.getElementById('deviceId')?.value;
        if (!deviceId) {
            showAlert('error', 'Please enter a Device ID');
            return;
        }

        this.stopMonitoring();
        this.fetchLatestData(deviceId);
        this.monitoringInterval = setInterval(() => {
            this.fetchLatestData(deviceId);
        }, 5000);

        showAlert('success', 'Device monitoring started');
    }

    stopMonitoring() {
        if (this.monitoringInterval) {
            clearInterval(this.monitoringInterval);
            this.monitoringInterval = null;
            showAlert('info', 'Device monitoring stopped');
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    new DeviceDataManager();
});
