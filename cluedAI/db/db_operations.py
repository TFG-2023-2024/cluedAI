import pymongo
from db.initial_data import initial_characters, initial_items, initial_locations

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
    
def setup_database():
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
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    # CREATE DATABASE
    db = myclient["cluedAI"]

    # CREATE COLLECTIONS
    characters_collection = db["characters"]
    items_collection = db["items"]
    locations_collection = db["locations"]

    # Insert initial data
    insert_data(initial_characters, characters_collection)
    insert_data(initial_items, items_collection)
    insert_data(initial_locations, locations_collection)
    
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

