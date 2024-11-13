from pymongo import MongoClient

try:
    # Create a MongoClient instance to connect to the local MongoDB server
    client = MongoClient('mongodb://localhost:27017')

    # Ping the server to check if the connection is established
    client.admin.command('ping')

    print("Successfully connected to MongoDB!")

except Exception as e:
    print("Could not connect to MongoDB:", e)
