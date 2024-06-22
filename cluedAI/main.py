import subprocess
import os
import time
from dotenv import load_dotenv
from db.db_operations import flush_db, setup_db
from screen_manager import basic_window

def start_mongodb():
    """
    Start MongoDB server.

    This function starts MongoDB using subprocess.Popen and waits for MongoDB to start.

    Returns:
    - mongodb_process (subprocess.Popen): The MongoDB process object.
    """
    mongodb_path = os.path.join(os.path.dirname(__file__), 'mongodb/bin/mongod')
    dbpath = os.path.join(os.path.dirname(__file__), 'mongodb/data')

    if not os.path.exists(dbpath):
        os.makedirs(dbpath)

    mongodb_process = subprocess.Popen([mongodb_path, '--dbpath', dbpath])
    time.sleep(5)  # Wait for MongoDB to initialize
    return mongodb_process

def main():
    """
    Main function to launch the application.

    This function loads environment variables, starts MongoDB, performs database operations,
    and initiates the GUI.
    """
    load_dotenv()  # Load environment variables from .env file
    #mongodb_process = start_mongodb()  
    
    #try:
    flush_db()  
    setup_db() 
    basic_window()  
    #finally:
        # Ensure MongoDB process is terminated when the application ends
        #mongodb_process.terminate()
        #mongodb_process.wait()

if __name__ == "__main__":
    main()
