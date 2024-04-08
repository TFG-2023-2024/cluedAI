import pymongo
import os
from db.initial_data import initial_characters, initial_items, initial_locations
from db.db_randomizers import randomize_archetypes, randomize_items, randomize_locations

def connect_db():
    """
    Connect to MongoDB and create the database if it doesn't exist.

    This function establishes a connection to MongoDB using the URI and database name
    specified in the environment variables. If the database doesn't exist, it creates it.

    Args:
    - None

    Returns:
    - db (pymongo.database.Database): The MongoDB database object.
    """
    try:
        # Connect to MongoDB
        myclient = pymongo.MongoClient(os.getenv('MONGODB_URI'))

        # Get database name from environment variables
        db_name = os.getenv('MONGODB_DB')

        # Create or get the database
        db = myclient[db_name]

        # CREATE COLLECTIONS
        characters_collection = db["characters"]
        items_collection = db["items"]
        locations_collection = db["locations"]
        users_collection = db["users"]

        print(f"Connected to MongoDB database: {db_name}")
        return db, characters_collection, items_collection, locations_collection, users_collection
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def insert_data(data, collection):
    """
    Insert initial data into a MongoDB collection.
    
    Args:
    - data (list): List of dictionaries containing the data to insert.
    - collection (pymongo.collection.Collection): The MongoDB collection to insert data into.
    
    Returns:
    - result (pymongo.results.InsertManyResult): The result of the insert operation.
    """
    try:
        result = collection.insert_many(data)
        print("Data inserted successfully.")
        return result
    except Exception as e:
        print(f"Error inserting data: {e}")
        return None
    
def setup_db():
    """
    Setup the MongoDB database by inserting initial data into respective collections.

    This function connects to a MongoDB database, inserts initial data into the
    "characters", "items", and "locations" collections, and prints a success message
    upon successful insertion.

    Args:
    - None

    Returns:
    - None
    """
    # CONNECT TO DATABASE
    _, characters_collection, items_collection, locations_collection, _ = connect_db()

    # Insert initial data
    insert_data(initial_characters, characters_collection)
    insert_data(initial_items, items_collection)
    insert_data(initial_locations, locations_collection)

def flush_db():
    """
    Flush all data from the MongoDB database.

    This function drops all collections in the MongoDB database, effectively
    removing all documents from the database.

    Args:
    - None

    Returns:
    - None
    """
    try:
        # Connect to MongoDB
        db = connect_db()

        # Drop collections
        db["characters"].drop()
        db["items"].drop()
        db["locations"].drop()

        print("Database flushed successfully.")
    except Exception as e:
        print(f"Error flushing database: {e}")
    
def insert_column_data(column_data, column_name, collection):
    """
    Insert data into a specific column of a MongoDB collection.

    Args:
    - column_data (list): List of values to insert into the specified column.
    - column_name (str): The name of the column where data will be inserted.
    - collection (pymongo.collection.Collection): The MongoDB collection to insert data into.

    Returns:
    - result (pymongo.results.InsertManyResult): The result of the insert operation.
    """
    try:
        bulk_operations = [pymongo.UpdateOne({"_id": data["_id"]}, {"$set": {column_name: data[column_name]}})
                           for data in column_data]
        result = collection.bulk_write(bulk_operations)
        print(f"Data inserted into {column_name} column successfully.")
        return result
    except Exception as e:
        print(f"Error inserting data into {column_name} column: {e}")
        return None

def randomize():
    """
    Randomizes character archetypes, locations, and items.

    Args:
    - None.

    Returns:
    - randomized_data (dict): Dictionary containing randomized character archetypes, locations, and items.
    """

    # CONNECT TO DATABASE
    _, characters_collection, items_collection, locations_collection, _ = connect_db()
    randomized_data = {}

    # Randomize character archetypes and update 
    randomize_archetypes(characters_collection)

    # Randomize locations
    randomized_data["locations"] = randomize_locations(locations_collection)

    # Randomize items with random location IDs
    randomized_data["items"] = randomize_items(items_collection, randomized_data["locations"])

    return randomized_data

def obtain_by_id(id, collection):
    """
    Fetches a database object by its ID from the given collection.

    Args:
    - id (any): The ID of the object to fetch.
    - collection (pymongo.collection.Collection): The MongoDB collection to search in.

    Returns:
    - db_object (dict): The database object corresponding to the provided ID.
                        Returns None if the object is not found.
    """
    try:
        # Find the object in the collection by its ID
        db_object = collection.find_one({"_id": id})
        return db_object
    except Exception as e:
        print(f"Error obtaining object by ID: {e}")
        return None