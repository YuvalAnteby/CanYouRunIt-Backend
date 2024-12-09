from pymongo import MongoClient

# Connect to MongoDB (this assumes MongoDB is running on localhost)
client = MongoClient("mongodb://localhost:27017/")
db = client["game_db"]  # Use your desired database name
