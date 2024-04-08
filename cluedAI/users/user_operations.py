from db.db_operations import connect_db

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
        _, _, _, _, users_collection = connect_db()

        # Insert the username into the users collection
        result = users_collection.insert_one({"username": username})
        print("User logged successfully.")
        return result
    except Exception as e:
        print(f"Error logging user: {e}")
        return None