import os
import time
import pymongo
from dotenv import load_dotenv
from db.db_operations import flush_db, setup_db
from screen_manager import basic_window

def start_mongodb(retries=3, delay=5):
    """
    Start MongoDB server.
    This function starts MongoDB using subprocess.Popen and waits for MongoDB to start.
    Returns:
    - mongodb_process (subprocess.Popen): The MongoDB process object.
    """
    load_dotenv()  # Load environment variables from .env file
    
    for attempt in range(1, retries + 1):
        try:
            # Attempt to connect to MongoDB
            myclient = pymongo.MongoClient(os.getenv('MONGODB_URI'))
            myclient.server_info()  # Trigger an exception if the server is not reachable
            print("Connected to MongoDB successfully.")
            return True
        except Exception as e:
            print(f"Error connecting to MongoDB (attempt {attempt} of {retries}): {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                return False

def main():
    """
    Main function to launch the application.

    This function loads environment variables, starts MongoDB, performs database operations,
    and initiates the GUI.
    """
    load_dotenv()  # Load environment variables from .env file
    
    if not start_mongodb():
        print("Error: No se pudo conectar a la base de datos después de varios intentos.")
        return



    flush_db()  
    setup_db() 
    basic_window()  



if __name__ == "__main__":
    main()
