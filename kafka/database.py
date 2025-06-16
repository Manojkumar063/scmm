from pymongo import MongoClient
# import os
# from dotenv import load_dotenv
# load_dotenv()
# MONGODB_URL=os.getenv("mongodb+srv://manojkumarpandi8:Mk271102@cluster0.xamvjdv.mongodb.net/supply_chain_db?retryWrites=true&w=majority")
# print(f"Connecting to MongoDB at {MONGODB_URL}")
 
client =MongoClient("mongodb+srv://manojkumarpandi8:mk271102@cluster0.xamvjdv.mongodb.net/")
print(client)
db = client['supply_chain_db']
users_data = db['users']
shipment_data = db['shipments']
device_data = db['devices']
# from pymongo import MongoClient
# from dotenv import load_dotenv
# import os
# import certifi
# import logging

# # Load .env variables
# load_dotenv()

# # Setup logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Get MongoDB URI from .env
# MONGODB_URL = os.getenv("MONGO_URL")  # Make sure your .env has MONGO_URL set
# DATABASE_NAME = "supply_chain_db"

# logger.info("Connecting to MongoDB Atlas...")

# try:
#     # Use TLS certificate from certifi for secure connection
#     client = MongoClient(MONGODB_URL, tlsCAFile=certifi.where())

#     # Connect to specific database
#     db = client[DATABASE_NAME]

#     # Collections
#     users_data = db['users']
#     shipment_data = db['shipments']
#     device_data = db['devices']

#     # Check connection
#     client.admin.command("ping")
#     logger.info("✅ MongoDB connected successfully.")
#     logger.info(f"Users count: {users_data.count_documents({})}")
#     logger.info(f"Shipments count: {shipment_data.count_documents({})}")
#     logger.info(f"Devices count: {device_data.count_documents({})}")

# except Exception as e:
#     logger.error(f"❌ MongoDB connection failed: {e}")
