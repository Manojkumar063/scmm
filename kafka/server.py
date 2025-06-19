"""
Simple TCP Server to simulate device telemetry data.

- Sends 15 JSON messages with random values
- Each message includes Battery Level, Device ID, Temperature, Route From/To
- Useful for testing client-side systems that receive sensor data
"""
# ────────────────────────────────────────────────────────────────────────────────
# Imports
# ────────────────────────────────────────────────────────────────────────────────
import socket
import json
import time
import random

# ────────────────────────────────────────────────────────────────────────────────
# Configuration
# ────────────────────────────────────────────────────────────────────────────────
PORT = 5050
SERVER = '192.168.60.35'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

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
    while True:
        route_from, route_to = random.sample(ROUTES, 2)
        
        device_number = random.randint(100000, 100020)  # 6-digit number
        device_id = f"IOT-DEV-{device_number}"  # Custom format

        data = {
            "Battery_Level": round(random.uniform(2.00, 5.00), 2),
            "Device_ID": device_id,
            "First_Sensor_temperature": round(random.uniform(10, 40.0), 1),
            "Route_From": route_from,
            "Route_To": route_to
        }

        # Encode data to bytes, add newline for TCP separation
        yield json.dumps(data).encode(FORMAT) + b'\n'

# ────────────────────────────────────────────────────────────────────────────────
# Start TCP Server
# ────────────────────────────────────────────────────────────────────────────────
def start_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)
        server.listen(2)
        print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
    except Exception as e:
        print(f"Socket setup failed: {e}")
        return

    try:
        conn, addr = server.accept()
        print(f"[CONNECTED] Client connected from {addr}")
        data_generator = generate_device_data()

        for _ in range(15):  # Send only 15 messages
            message = next(data_generator)
            conn.sendall(message)
            print("[SENT]:", message.decode(FORMAT).strip())
            time.sleep(2)  # Sleep 2 seconds between messages

    except Exception as e:
        print(f"[ERROR] During communication: {e}")

    finally:
        conn.close()
        server.close()
        print("[CLOSED] Server connections closed")

# ────────────────────────────────────────────────────────────────────────────────
# Entry Point
# ────────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    start_server()
