from db.db_operations import connect_db

import pymongo
from pymongo.errors import DuplicateKeyError

def log_user(username):
    """
    Logs a user by inserting their username into the database collection.

    Args:
    - username (str): The username to log.

    Returns:
    - result (pymongo.results.InsertOneResult): The result of the insert operation.
    """
    try:
        # Connect to the users collection in the database
        _, _, _, _, users_collection, _ = connect_db()

        # Create a unique index on the 'username' field
        users_collection.create_index([('username', pymongo.ASCENDING)], unique=True)

        # Insert the username into the users collection
        result = users_collection.insert_one({"username": username})
        print("User logged successfully.")
        return result
    except DuplicateKeyError:
        print("Error: Username already exists.")
        return None
    except Exception as e:
        print(f"Error logging user: {e}")
        return None
    
def insert_character(username, data):
    """
    Inserts character data into the database for the given username.

    Args:
    - username (str): The username to search for in the database.
    - data (dict): A dictionary containing character data including name, age, gender, and appearance.

    Returns:
    - result (pymongo.results.InsertOneResult): The result of the insert operation.
    """
    try:
        # Connect to the users collection in the database
        _, _, _, _, users_collection, _ = connect_db()

        # Find the user by username
        user_query = {"username": username}
        user = users_collection.find_one(user_query)

        if user:
            # Update the user document with character data
            update_query = {"$set": {
                "username": username,
                "Name": data.get("Name", ""),
                "Age": data.get("Age", ""),
                "Gender": data.get("Gender", ""),
                "Appearance": data.get("Appearance", "")
            }}
            result = users_collection.update_one(user_query, update_query)
            print("Character data inserted successfully.")
            return result
        else:
            print("Error: Username not found.")
            return None
    except Exception as e:
        print(f"Error inserting character data: {e}")
        return None