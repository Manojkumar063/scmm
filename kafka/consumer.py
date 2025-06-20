# ────────────────────────────────────────────────────────────────────────────────
# Imports
# ────────────────────────────────────────────────────────────────────────────────
from kafka import KafkaConsumer
import json
import logging
import time

from database import device_data

# ────────────────────────────────────────────────────────────────────────────────
# Logging Configuration
# ────────────────────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ────────────────────────────────────────────────────────────────────────────────
# Kafka Configuration
# ────────────────────────────────────────────────────────────────────────────────
KAFKA_TOPIC = 'device-data'
KAFKA_BOOTSTRAP_SERVERS = '192.168.60.35:9092'

# ────────────────────────────────────────────────────────────────────────────────
# Kafka Consumer Factory     
# ────────────────────────────────────────────────────────────────────────────────
def create_consumer(max_retries=5, retry_delay=5):
    retry_count = 0 

    while retry_count < max_retries:
        try:
            consumer = KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='device-data-consumers',
                max_poll_interval_ms=300000,
                request_timeout_ms=60000,
                max_poll_records=10,
                retry_backoff_ms=1000,
                api_version=(2, 5, 0),
                security_protocol='PLAINTEXT'
            )
            logger.info(f"Successfully connected to Kafka broker at {KAFKA_BOOTSTRAP_SERVERS}")
            return consumer

        except Exception as e:
            retry_count += 1
            logger.warning(f"Attempt {retry_count}/{max_retries} failed to connect to Kafka: {str(e)}")

            if retry_count < max_retries:
                time.sleep(retry_delay)

    logger.error(f"Failed to connect to Kafka after {max_retries} attempts")
    raise ConnectionError("Could not establish connection to Kafka broker")

# ────────────────────────────────────────────────────────────────────────────────
# Kafka Message Processing Loop
# ────────────────────────────────────────────────────────────────────────────────
def process_messages(consumer):
    try:
        while True:
            try:
                messages = consumer.poll(timeout_ms=1000)

                if not messages:
                    logger.debug("No messages received, waiting...")
                    continue

                for _, partition_messages in messages.items():
                    for message in partition_messages:
                        try:
                            data = message.value
                            logger.info(f"Received message: {json.dumps(data, indent=2)}")

                            device_data.insert_one(data)
                            logger.info("Successfully saved to MongoDB")

                        except Exception as e:
                            logger.error(f"Error processing message: {str(e)}")

            except Exception as poll_error:
                logger.error(f"Error during poll: {str(poll_error)}")
                time.sleep(5)  # Delay before retrying

    except KeyboardInterrupt:
        logger.info("Stopped by user")

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

    finally:
        consumer.close()
        logger.info("Consumer closed")
                                                                                        
# ────────────────────────────────────────────────────────────────────────────────
# Entrypoint         
# ────────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:     
        consumer = create_consumer()
        process_messages(consumer)

    except Exception as e:
        logger.error(f"Fatal error in consumer: {str(e)}")

# ────────────────────────────────────────────────────────────────────────────────
# Imports
# ────────────────────────────────────────────────────────────────────────────────
from kafka import KafkaConsumer  # Kafka consumer for reading messages from Kafka
import json                     # Used for decoding JSON messages
import logging                  # For logging informational and error messages
import time                     # For retry delay and time-based operations

from database import device_data  # MongoDB collection reference for storing device data

# ────────────────────────────────────────────────────────────────────────────────
# Logging Configuration
# ────────────────────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)  # Set logging level to INFO
logger = logging.getLogger(__name__)     # Create a logger instance with the module name

# ────────────────────────────────────────────────────────────────────────────────
# Kafka Configuration
# ────────────────────────────────────────────────────────────────────────────────
KAFKA_TOPIC = 'device-data'                      # Topic to consume messages from
KAFKA_BOOTSTRAP_SERVERS = '192.168.60.35:9092'   # Kafka broker IP and port

# ────────────────────────────────────────────────────────────────────────────────
# Kafka Consumer Factory
# ────────────────────────────────────────────────────────────────────────────────
def create_consumer(max_retries=5, retry_delay=5):
    retry_count = 0  # Initialize retry counter

    while retry_count < max_retries:  # Retry loop
        try:
            # Attempt to create a Kafka consumer instance
            consumer = KafkaConsumer(
                KAFKA_TOPIC,  # Subscribe to the 'device-data' topic
                bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],  # Kafka broker address
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),  # Deserialize JSON messages
                auto_offset_reset='earliest',  # Start from the beginning if no offset is committed
                enable_auto_commit=True,  # Automatically commit offsets
                group_id='device-data-consumers',  # Consumer group ID
                max_poll_interval_ms=300000,  # Max time allowed between polls
                request_timeout_ms=60000,  # Timeout for Kafka request
                max_poll_records=10,  # Max number of records returned in one poll
                retry_backoff_ms=1000,  # Backoff time between retries on fetch
                api_version=(2, 5, 0),  # Kafka broker version
                security_protocol='PLAINTEXT'  # No encryption
            )
            logger.info(f"Successfully connected to Kafka broker at {KAFKA_BOOTSTRAP_SERVERS}")
            return consumer  # Return the configured consumer

        except Exception as e:
            # On failure, log warning and increment retry count
            retry_count += 1
            logger.warning(f"Attempt {retry_count}/{max_retries} failed to connect to Kafka: {str(e)}")

            if retry_count < max_retries:
                time.sleep(retry_delay)  # Wait before next retry

    logger.error(f"Failed to connect to Kafka after {max_retries} attempts")
    raise ConnectionError("Could not establish connection to Kafka broker")

# ────────────────────────────────────────────────────────────────────────────────
# Kafka Message Processing Loop
# ────────────────────────────────────────────────────────────────────────────────
def process_messages(consumer):
    try:
        while True:  # Infinite loop to keep polling messages
            try:
                messages = consumer.poll(timeout_ms=1000)  # Poll Kafka for new messages

                if not messages:  # If no messages are returned
                    logger.debug("No messages received, waiting...")
                    continue  # Continue polling

                # Loop through each partition and its list of messages
                for _, partition_messages in messages.items():
                    for message in partition_messages:
                        try:
                            data = message.value  # Extract the message payload (already JSON deserialized)
                            logger.info(f"Received message: {json.dumps(data, indent=2)}")

                            device_data.insert_one(data)  # Insert the message into MongoDB
                            logger.info("Successfully saved to MongoDB")

                        except Exception as e:
                            logger.error(f"Error processing message: {str(e)}")  # Log any processing errors

            except Exception as poll_error:
                logger.error(f"Error during poll: {str(poll_error)}")  # Log polling errors
                time.sleep(5)  # Wait before trying to poll again

    except KeyboardInterrupt:
        logger.info("Stopped by user")  # Handle graceful exit on Ctrl+C

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")  # Catch-all for any unexpected exceptions

    finally:
        consumer.close()  # Always close the consumer on exit
        logger.info("Consumer closed")

# ────────────────────────────────────────────────────────────────────────────────
# Entrypoint
# ────────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        consumer = create_consumer()  # Create a Kafka consumer
        process_messages(consumer)    # Start processing messages

    except Exception as e:
        logger.error(f"Fatal error in consumer: {str(e)}")  # Log any fatal error during setup or execution
