from flask import Flask, jsonify, request
import requests
import json
import os
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

JOKE_API_URL = "https://v2.jokeapi.dev/joke/Any?type=single,twopart&lang=en&amount=10"
JOKES_FILE_PATH = os.path.join(os.path.dirname(__file__), 'jokes.json')

# MongoDB connection details
MONGO_URI = "mongodb://localhost:27017"  # Update if your MongoDB URI is different
MONGO_DB = "jokesDB"
MONGO_COLLECTION = "jokes"

# Set up MongoDB client
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

def fetch_jokes(amount=100):
    jokes = []
    while amount > 0:
        # Determine how many jokes to request in this iteration (max 10)
        batch_size = min(amount, 10)
        
        # Fetch a batch of jokes
        response = requests.get(JOKE_API_URL)
        if response.status_code == 200:
            jokes_data = response.json().get('jokes', [])
            jokes.extend(jokes_data)
            amount -= len(jokes_data)
        else:
            print(f"Failed to fetch jokes. Status code: {response.status_code}")
            break  # Exit if there is an issue with the request
    
    # Save jokes to JSON file
    save_jokes_to_file(jokes)
    # Save jokes to MongoDB
    save_jokes_to_mongodb(jokes)
    return jokes

def save_jokes_to_file(jokes):
    try:
        with open(JOKES_FILE_PATH, 'w', encoding='utf-8') as file:
            json.dump({"jokes": jokes}, file, ensure_ascii=False, indent=4)
        print(f"Jokes saved to {JOKES_FILE_PATH}")
    except Exception as e:
        print(f"Error saving jokes to JSON file: {e}")

def save_jokes_to_mongodb(jokes):
    try:
        # Insert jokes into MongoDB collection
        if jokes:
            collection.insert_many(jokes)
            print(f"Successfully saved {len(jokes)} jokes to MongoDB")
    except Exception as e:
        print(f"Error saving jokes to MongoDB: {e}")

# Function to convert ObjectId to string for JSON serialization
def serialize_object_id(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj

@app.route('/')
def home():
    return "Welcome to the Joke API! Use /api/jokes?amount=<number> to fetch jokes."

@app.route('/api/jokes', methods=['GET'])
def get_jokes():
    # Get the 'amount' parameter from the request (default is 10 jokes)
    amount = request.args.get('amount', default=10, type=int)
    
    # Fetch the jokes
    jokes = fetch_jokes(amount)
    
    # Convert ObjectId to string for all jokes in the response
    jokes_serializable = [json.dumps(joke, default=serialize_object_id) for joke in jokes]
    
    if jokes:
        return jsonify({"jokes": jokes_serializable, "count": len(jokes)}), 200
    else:
        return jsonify({"error": "Failed to fetch jokes"}), 500

if __name__ == "__main__":
    app.run(debug=True)
