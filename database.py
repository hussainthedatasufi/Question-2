import pymongo
from pymongo import MongoClient
import os

def get_db():
    # Setup MongoDB connection
    client = MongoClient("mongodb://localhost:27017/")
    db = client.jokes_database  # This is the database where jokes will be stored
    return db.jokes_collection