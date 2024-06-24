import subprocess
import os
import time
from dotenv import load_dotenv
from db.db_operations import flush_db, setup_db
from screen_manager import basic_window


def main():
    """
    Main function to launch the application.

    This function loads environment variables, starts MongoDB, performs database operations,
    and initiates the GUI.
    """
    load_dotenv()  # Load environment variables from .env file
    

    flush_db()  
    setup_db() 
    basic_window()  


if __name__ == "__main__":
    main()
