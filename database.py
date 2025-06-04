from pymongo import MongoClient
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Get MongoDB connection details from environment variables
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "supply_chain_db")

# Initialize variables
client = None
db = None
users_data = None
device_data = None
shipment_data = None

try:
    # Create MongoDB client with improved configuration
    client = MongoClient(
        MONGODB_URL,
        serverSelectionTimeoutMS=5000,  # 5 second timeout
        connectTimeoutMS=5000,
        socketTimeoutMS=5000,
        maxPoolSize=50,
        retryWrites=True
    )
    
    # Get database
    db = client[DATABASE_NAME]
    
    # Test connection quickly
    client.admin.command('ping')
    
    # Collections
    users_data = db.users
    device_data = db.devices
    shipment_data = db.shipments
    
    # Test collections by checking if they exist
    collection_names = db.list_collection_names()
    logger.info(f"Available collections: {collection_names}")
    
    # Create indexes for better performance
    try:
        users_data.create_index("email", unique=True)
        shipment_data.create_index("shipment_number", unique=True)
        shipment_data.create_index("delivery_number", unique=True)
        shipment_data.create_index("user_id")
        device_data.create_index("device_id")
        logger.info("Database indexes created successfully")
    except Exception as index_error:
        logger.warning(f"Index creation error (may already exist): {index_error}")
    
    logger.info(f"Successfully connected to MongoDB database: {DATABASE_NAME}")
    logger.info(f"Database URL: {MONGODB_URL}")
    
    # Test basic operations
    user_count = users_data.count_documents({})
    shipment_count = shipment_data.count_documents({})
    device_count = device_data.count_documents({})
    
    logger.info(f"Current document counts - Users: {user_count}, Shipments: {shipment_count}, Devices: {device_count}")
    
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    logger.error(f"MongoDB URL attempted: {MONGODB_URL}")
    logger.error(f"Database name: {DATABASE_NAME}")
    
    # Set all to None to handle gracefully in routes
    client = None
    db = None
    users_data = None
    device_data = None
    shipment_data = None


def get_database_status():
    """Check database connection status."""
    try:
        if client is None:
            return {"status": "disconnected", "message": "No database connection"}
        
        client.admin.command('ping')
        return {"status": "connected", "message": f"Connected to {DATABASE_NAME}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def reconnect_database():
    """Attempt to reconnect to database."""
    global client, db, users_data, device_data, shipment_data
    
    try:
        if client:
            client.close()
        
        client = MongoClient(
            MONGODB_URL,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=5000,
            maxPoolSize=50,
            retryWrites=True
        )
        
        db = client[DATABASE_NAME]
        client.admin.command('ping')
        
        users_data = db.users
        device_data = db.devices
        shipment_data = db.shipments
        
        logger.info("Database reconnection successful")
        return True
        
    except Exception as e:
        logger.error(f"Database reconnection failed: {e}")
        return False