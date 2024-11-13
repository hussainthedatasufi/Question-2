# JokeAPI Flask Project

## Requirements

- Python 3.x
- MongoDB (installed and running on localhost)

## Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd joke-api
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run MongoDB locally (if you haven't already):
    ```bash
    mongod
    ```

4. Run the Flask app:
    ```bash
    python app.py
    ```

## Usage

To fetch jokes from the JokeAPI and store them in MongoDB, visit the following endpoint:
GET http://127.0.0.1:5000/fetch_and_store_jokes

markdown
Copy code

This will fetch 100 jokes, process the necessary information, and store them in the `jokes_database` MongoDB database.

## Notes

- The API will store the jokes in the `jokes_collection` MongoDB collection.
Step 7: Running the Application
Once everything is set up, run the Flask application:

bash
Copy code
python app.py
The API will be accessible at http://127.0.0.1:5000. You can call the /fetch_and_store_jokes endpoint to fetch jokes from JokeAPI, process them, and store them in MongoDB.