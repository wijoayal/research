from pymongo import MongoClient
from datetime import datetime

mongo_details = "mongodb+srv://root:root@cluster0.6b2ol.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongo_details)


db_network_data = client.network_data
collection_routers = db_network_data.routers
collection_routers_state = db_network_data.routers_state
collection_routers_history = db_network_data.routers_history