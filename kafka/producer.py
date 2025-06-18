# ────────────────────────────────────────────────────────────────────────────────
# Imports
# ────────────────────────────────────────────────────────────────────────────────
import socket
import json
import time
from kafka import KafkaProducer

# ────────────────────────────────────────────────────────────────────────────────
# TCP Configuration
# ────────────────────────────────────────────────────────────────────────────────
SERVER_HOST = '192.168.60.35'
SERVER_PORT = 5050
FORMAT = 'utf-8'

# ────────────────────────────────────────────────────────────────────────────────
# Kafka Configuration
# ────────────────────────────────────────────────────────────────────────────────
KAFKA_TOPIC = 'device-data'
KAFKA_BOOTSTRAP_SERVERS = '192.168.60.35:9092'

# ────────────────────────────────────────────────────────────────────────────────
# Connect to TCP Server
# ────────────────────────────────────────────────────────────────────────────────
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print(f"[CONNECTED] to TCP server at {SERVER_HOST}:{SERVER_PORT}")
except Exception as e:
    print(f"[ERROR] Could not connect to TCP server: {e}")
    exit(1)

# ────────────────────────────────────────────────────────────────────────────────
# Initialize Kafka Producer
# ────────────────────────────────────────────────────────────────────────────────
try:
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        retries=5
    )
    print("[KAFKA] Producer ready")
except Exception as e:
    print(f"[ERROR] Kafka producer failed: {e}")
    client_socket.close()
    exit(1)

# ────────────────────────────────────────────────────────────────────────────────
# Read from TCP Socket and Send to Kafka
# ────────────────────────────────────────────────────────────────────────────────
try:
    while True:
        data = client_socket.recv(1024)
        if not data:
            print("[DISCONNECTED] No data from server")
            break

        try:
            decoded = data.decode(FORMAT)
            json_data = json.loads(decoded)
            print("[RECEIVED]", json_data)

            producer.send(KAFKA_TOPIC, value=json_data)
            print("[KAFKA] Sent to topic:", KAFKA_TOPIC)

        except json.JSONDecodeError:
            print("[ERROR] Invalid JSON:", decoded)
        except Exception as e:
            print(f"[ERROR] Kafka send failed: {e}")

# ────────────────────────────────────────────────────────────────────────────────
# Graceful Shutdown
# ────────────────────────────────────────────────────────────────────────────────
except KeyboardInterrupt:
    print("[EXIT] Interrupted by user")

finally:
    client_socket.close()
    producer.flush()
    producer.close()
    print("[CLOSED] All connections closed")
