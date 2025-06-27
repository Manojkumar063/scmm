"""
Simple TCP Server to simulate device telemetry data.

- Sends JSON messages with random values continuously
- Each message includes Battery Level, Device ID, Temperature, Route From/To
- Useful for testing client-side systems that receive sensor data
- Handles multiple client connections
"""
# ────────────────────────────────────────────────────────────────────────────────
# Imports
# ────────────────────────────────────────────────────────────────────────────────
import socket
import json
import time
import random
import threading
import os

# ────────────────────────────────────────────────────────────────────────────────
# Configuration
# ────────────────────────────────────────────────────────────────────────────────
PORT = int(os.getenv('SERVER_PORT', '8000'))  # Use environment variable or default to 8000
SERVER = '0.0.0.0'  # Bind to all interfaces for Docker compatibility
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
MESSAGE_INTERVAL = 2  # Seconds between messages

# Predefined simulation routes
ROUTES = [
    'New York, USA',
    'Chennai, India',
    'Bengaluru, India',
    'London, UK',
    'Frankfurt, Germany',
    'Berlin, Germany',
    'Paris, France',
    'Tokyo, Japan',
    'Seoul, South Korea',
    'Beijing, China',
    'Shanghai, China',
    'Hong Kong, China',
    'Singapore',
    'Dubai, UAE',
    'Sydney, Australia',
    'Melbourne, Australia',
    'Auckland, New Zealand',
    'Los Angeles, USA',
    'San Francisco, USA',
    'Miami, USA',
    'Toronto, Canada',
    'Vancouver, Canada',
    'Montreal, Canada',
    'Mexico City, Mexico',
    'São Paulo, Brazil',
    'Buenos Aires, Argentina',
    'Lima, Peru',
    'Bogotá, Colombia',
    'Caracas, Venezuela',
    'Santiago, Chile',
    'Quito, Ecuador'
]

# ────────────────────────────────────────────────────────────────────────────────
# Data Generator
# ────────────────────────────────────────────────────────────────────────────────
def generate_device_data():
    """Generate random device telemetry data"""
    route_from, route_to = random.sample(ROUTES, 2)
        
    device_number = random.randint(100000, 100020)  # 6-digit number
    device_id = f"IOT-DEV-{device_number}"  # Custom format

    data = {
        "Battery_Level": round(random.uniform(2.00, 5.00), 2),
        "Device_ID": device_id,
        "First_Sensor_temperature": round(random.uniform(10, 40.0), 1),
        "Route_From": route_from,
        "Route_To": route_to,
        "timestamp": time.time()
    }

    return data

# ────────────────────────────────────────────────────────────────────────────────
# Handle Client Connection
# ────────────────────────────────────────────────────────────────────────────────
def handle_client(conn, addr):
    """Handle individual client connection"""
    print(f"[NEW CONNECTION] Client connected from {addr}")
    
    try:
        message_count = 0
        while True:
            # Generate and send data
            data = generate_device_data()
            message = json.dumps(data) + '\n'  # Add newline for message separation
            
            try:
                conn.sendall(message.encode(FORMAT))
                message_count += 1
                print(f"[SENT to {addr}] Message {message_count}: {data['Device_ID']} - Temp: {data['First_Sensor_temperature']}°C")
                
                # Sleep between messages
                time.sleep(MESSAGE_INTERVAL)
                
            except socket.error as e:
                print(f"[DISCONNECTED] Client {addr} disconnected: {e}")
                break
                
    except Exception as e:
        print(f"[ERROR] Error handling client {addr}: {e}")
    
    finally:
        conn.close()
        print(f"[CLOSED] Connection with {addr} closed")

# ────────────────────────────────────────────────────────────────────────────────
# Start TCP Server
# ────────────────────────────────────────────────────────────────────────────────
def start_server():
    """Start the TCP server and handle multiple clients"""
    server = None
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow address reuse
        server.bind(ADDR)
        server.listen(5)  # Allow up to 5 pending connections
        print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
        print(f"[CONFIG] Message interval: {MESSAGE_INTERVAL} seconds")
        
        while True:
            try:
                conn, addr = server.accept()
                
                # Handle each client in a separate thread
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.daemon = True  # Thread will die when main program exits
                thread.start()
                
            except socket.error as e:
                print(f"[ERROR] Error accepting connection: {e}")
                continue
                
    except Exception as e:
        print(f"[ERROR] Server setup failed: {e}")
        return
    
    except KeyboardInterrupt:
        print("\n[EXIT] Server shutdown requested")
    
    finally:
        if server:
            server.close()
        print("[CLOSED] Server socket closed")

# ────────────────────────────────────────────────────────────────────────────────
# Health Check Function
# ────────────────────────────────────────────────────────────────────────────────
def health_check():
    """Simple health check - test if server port is accessible"""
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.settimeout(1)
        result = test_socket.connect_ex(('localhost', PORT))
        test_socket.close()
        return result == 0
    except:
        return False

# ────────────────────────────────────────────────────────────────────────────────
# Entry Point
# ────────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"[STARTUP] Starting TCP Telemetry Server on port {PORT}")
    print(f"[INFO] Server will send data every {MESSAGE_INTERVAL} seconds")
    start_server()