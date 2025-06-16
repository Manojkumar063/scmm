import socket
import json
import time
import random

PORT = 5050
SERVER = '192.168.60.35'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# Routes for simulation
ROUTES = ['Newyork,USA', 'Chennai,India', 'Bengaluru,India', 'London,UK']

def generate_device_data():
    while True:
        route_from, route_to = random.sample(ROUTES, 2)
        data = {
            "Battery_Level": round(random.uniform(2.00, 5.00), 2),
            "Device_ID": random.randint(1150, 1158),
            "First_Sensor_temperature": round(random.uniform(10, 40.0), 1),
            "Route_From": route_from,
            "Route_To": route_to
        }
        yield json.dumps(data).encode(FORMAT) + b'\n'  # newline for message boundary


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

        for _ in range(15):  # Send only 5 messages
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

if __name__ == "__main__":
    start_server()


