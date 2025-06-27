# ────────────────────────────────────────────────────────────────────────────────
# Imports
# ────────────────────────────────────────────────────────────────────────────────
import socket
import json
import time
import os
from kafka import KafkaProducer

# ────────────────────────────────────────────────────────────────────────────────
# TCP Configuration
# ────────────────────────────────────────────────────────────────────────────────
SERVER_HOST = os.getenv('SERVER_HOST', 'kafka_server')  # Use container name
SERVER_PORT = int(os.getenv('SERVER_PORT', '8000'))     # Updated to match server
FORMAT = 'utf-8'

# ────────────────────────────────────────────────────────────────────────────────
# Kafka Configuration
# ────────────────────────────────────────────────────────────────────────────────
KAFKA_TOPIC = 'device-data'
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BROKER', 'kafka:9092')  # Use container name

print(f"[CONFIG] Connecting to TCP Server: {SERVER_HOST}:{SERVER_PORT}")
print(f"[CONFIG] Kafka Bootstrap Servers: {KAFKA_BOOTSTRAP_SERVERS}")

# ────────────────────────────────────────────────────────────────────────────────
# Connect to TCP Server
# ────────────────────────────────────────────────────────────────────────────────
def connect_to_server():
    max_retries = 10
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(10)  # 10 second timeout
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            print(f"[CONNECTED] to TCP server at {SERVER_HOST}:{SERVER_PORT}")
            return client_socket
        except Exception as e:
            print(f"[ERROR] Attempt {attempt + 1}/{max_retries} - Could not connect to TCP server: {e}")
            if attempt < max_retries - 1:
                print(f"[RETRY] Waiting {retry_delay} seconds before retry...")
                time.sleep(retry_delay)
            else:
                print(f"[FAILED] Could not connect to TCP server after {max_retries} attempts")
                return None

# ────────────────────────────────────────────────────────────────────────────────
# Initialize Kafka Producer
# ────────────────────────────────────────────────────────────────────────────────
def create_kafka_producer():
    max_retries = 10
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                retries=5,
                request_timeout_ms=30000,
                retry_backoff_ms=1000
            )
            print("[KAFKA] Producer ready")
            return producer
        except Exception as e:
            print(f"[ERROR] Attempt {attempt + 1}/{max_retries} - Kafka producer failed: {e}")
            if attempt < max_retries - 1:
                print(f"[RETRY] Waiting {retry_delay} seconds before retry...")
                time.sleep(retry_delay)
            else:
                print(f"[FAILED] Could not create Kafka producer after {max_retries} attempts")
                return None

# ────────────────────────────────────────────────────────────────────────────────
# Main Processing Loop
# ────────────────────────────────────────────────────────────────────────────────
def main():
    # Connect to TCP Server
    client_socket = connect_to_server()
    if not client_socket:
        exit(1)
    
    # Initialize Kafka Producer
    producer = create_kafka_producer()
    if not producer:
        client_socket.close()
        exit(1)
    
    # ────────────────────────────────────────────────────────────────────────────────
    # Read from TCP Socket and Send to Kafka
    # ────────────────────────────────────────────────────────────────────────────────
    try:
        buffer = ""  # Buffer for incomplete messages
        
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    print("[DISCONNECTED] No data from server")
                    break

                # Decode and add to buffer
                buffer += data.decode(FORMAT)
                
                # Process complete messages (separated by newlines)
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    
                    if not line:
                        continue
                    
                    try:
                        json_data = json.loads(line)
                        print("[RECEIVED]", json_data)

                        # Send to Kafka
                        future = producer.send(KAFKA_TOPIC, value=json_data)
                        # Wait for send to complete
                        record_metadata = future.get(timeout=10)
                        print(f"[KAFKA] Sent to topic: {KAFKA_TOPIC}, partition: {record_metadata.partition}, offset: {record_metadata.offset}")

                    except json.JSONDecodeError as e:
                        print(f"[ERROR] Invalid JSON: {line[:100]}... Error: {e}")
                    except Exception as e:
                        print(f"[ERROR] Kafka send failed: {e}")
                        
            except socket.timeout:
                print("[TIMEOUT] No data received, continuing...")
                continue
            except Exception as e:
                print(f"[ERROR] Socket error: {e}")
                break

    # ────────────────────────────────────────────────────────────────────────────────
    # Graceful Shutdown
    # ────────────────────────────────────────────────────────────────────────────────
    except KeyboardInterrupt:
        print("[EXIT] Interrupted by user")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
    finally:
        print("[CLEANUP] Closing connections...")
        if client_socket:
            client_socket.close()
        if producer:
            producer.flush()
            producer.close()
        print("[CLOSED] All connections closed")

# ────────────────────────────────────────────────────────────────────────────────
# Entry Point
# ────────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()