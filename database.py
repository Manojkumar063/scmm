# ────────────────────────────────────────────────────────────────────────────────
# Imports
# ────────────────────────────────────────────────────────────────────────────────

import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi

# ────────────────────────────────────────────────────────────────────────────────
# Load Environment Variables
# ────────────────────────────────────────────────────────────────────────────────

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# ────────────────────────────────────────────────────────────────────────────────
# Logger Configuration
# ────────────────────────────────────────────────────────────────────────────────

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/scmm_app.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

logger.info(f"Connecting to MongoDB at {MONGODB_URL} with database {DATABASE_NAME}")

# ────────────────────────────────────────────────────────────────────────────────
# Global MongoDB Variables   
# ────────────────────────────────────────────────────────────────────────────────

client = None
db = None
users_data = None
shipment_data = None
device_data = None

# ────────────────────────────────────────────────────────────────────────────────
# Connect to MongoDB    
# ────────────────────────────────────────────────────────────────────────────────

try:
    client = MongoClient(
        MONGODB_URL,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000,
        socketTimeoutMS=5000,
        maxPoolSize=50,
        tlsCAFile=certifi.where()#FOR SECURE CONNECTION ATLAS
    )

    db = client[DATABASE_NAME]
    client.admin.command("ping")
    logger.info(f"✅ Connected to MongoDB database: {DATABASE_NAME}")



    # Collections
    users_data = db["users"]
    shipment_data = db["shipments"]
    device_data = db["devices"]

    # Create indexes
    try:
        users_data.create_index("email", unique=True)
        shipment_data.create_index("shipment_number", unique=True)
        shipment_data.create_index("delivery_number",unique=True)
        shipment_data.create_index("user_id")
        device_data.create_index("device_id")
        logger.info("✅ Indexes created successfully")
    except Exception as index_err:
        logger.warning(f"⚠️ Index creation issue: {index_err}")

    # Log document counts
    logger.info(
        f"📦 Document counts — Users: {users_data.count_documents({})}, "
        f"Shipments: {shipment_data.count_documents({})}, "
        f"Devices: {device_data.count_documents({})}"
    )

except Exception as e:
    logger.error(f"❌ MongoDB connection failed: {e}")
    logger.error(f"🔗 Attempted URL: {MONGODB_URL}")
    client = db = users_data = shipment_data = device_data = None

# ────────────────────────────────────────────────────────────────────────────────
# Utility Functions                                        
# ────────────────────────────────────────────────────────────────────────────────

def get_database():
    """
    Returns the MongoDB database instance.
    Raises RuntimeError if connection is not established.
    """
    if db is None:
        raise RuntimeError("Database connection not initialized")
    return db

def get_database_status():
    """
    Checks and returns the status of the MongoDB connection.
    """
    try:
        if client is None:
            return {"status": "disconnected", "message": "No MongoDB connection"}
        client.admin.command("ping")
        return {"status": "connected", "message": f"Connected to {DATABASE_NAME}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def reconnect_database():
    """
    Reconnects to MongoDB and reinitializes collections.
    Returns True if successful, otherwise False.
    """
    global client, db, users_data, shipment_data, device_data
    try:
        if client:
            client.close()

        client = MongoClient(
            MONGODB_URL,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=5000,
            maxPoolSize=50,
            tlsCAFile=certifi.where()
        )

        db = client[DATABASE_NAME]
        client.admin.command("ping")

        users_data = db["users"]
        shipment_data = db["shipments"]
        device_data = db["devices"]

        logger.info("🔁 MongoDB reconnected successfully.")
        return True

    except Exception as e:
        logger.error(f"❌ Reconnection failed: {e}")
        return False
