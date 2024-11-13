from flask import Flask, jsonify
import requests
import json
import os
from pymongo import MongoClient

app = Flask(__name__)

JOKE_API_URL = "https://v2.jokeapi.dev/joke/Any?type=single,twopart&lang=en&amount=10"
JOKES_FILE_PATH = os.path.join(os.path.dirname(__file__), 'jokes.json')

# MongoDB connection details (update with your connection string or credentials)
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "jokes_db"
COLLECTION_NAME = "jokes"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

def fetch_jokes():
    try:
        response = requests.get(JOKE_API_URL)
        response.raise_for_status()  # This will raise an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching jokes: {e}")
        return None

def process_jokes(jokes):
    processed_jokes = []
    if jokes and 'jokes' in jokes:
        for joke in jokes['jokes']:
            processed_joke = {
                'category': joke.get('category'),
                'type': joke.get('type'),
                'joke': joke.get('joke') if joke.get('type') == 'single' else None,
                'setup': joke.get('setup') if joke.get('type') == 'twopart' else None,
                'delivery': joke.get('delivery') if joke.get('type') == 'twopart' else None,
                'flags_nsfw': joke.get('flags', {}).get('nsfw', False),
                'flags_political': joke.get('flags', {}).get('political', False),
                'flags_sexist': joke.get('flags', {}).get('sexist', False),
                'safe': joke.get('safe', False),
                'lang': joke.get('lang')
            }
            processed_jokes.append(processed_joke)
    return processed_jokes

def store_jokes(jokes):
    try:
        # Save to JSON file (optional)
        with open(JOKES_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(jokes, f, ensure_ascii=False, indent=4)
        print(f"Jokes saved to {JOKES_FILE_PATH}")

        # Insert jokes into MongoDB
        if jokes:
            result = collection.insert_many(jokes)
            print(f"Jokes saved to MongoDB with IDs: {result.inserted_ids}")
            return True
        else:
            print("No jokes to insert into MongoDB.")
            return False
    except Exception as e:
        print(f"Error saving jokes to MongoDB: {e}")
        return False

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Joke Fetcher API!'}), 200

@app.route('/fetch_and_store_jokes', methods=['GET'])
def fetch_and_store_jokes():
    jokes_data = fetch_jokes()
    
    if jokes_data:
        processed_jokes = process_jokes(jokes_data)
        if processed_jokes:
            saved = store_jokes(processed_jokes)
            if saved:
                return jsonify({'message': 'Jokes fetched and saved to MongoDB and JSON file successfully!', 'jokes_saved': len(processed_jokes)}), 200
            else:
                return jsonify({'message': 'Failed to save jokes to MongoDB and JSON file'}), 500
        else:
            return jsonify({'message': 'No jokes to process'}), 500
    else:
        return jsonify({'message': 'Failed to fetch jokes from the API'}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
