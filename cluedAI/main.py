import subprocess
import os
import time
from dotenv import load_dotenv
from db.db_operations import flush_db, setup_db, randomize
from characters.character_operations import create_character
from initial_gui import start_screen

def start_mongodb():
    mongodb_path = os.path.join(os.path.dirname(__file__), 'mongodb/bin/mongod')
    dbpath = os.path.join(os.path.dirname(__file__), 'mongodb/data')
    if not os.path.exists(dbpath):
        os.makedirs(dbpath)
    
    # Inicia MongoDB
    mongodb_process = subprocess.Popen([mongodb_path, '--dbpath', dbpath])
    time.sleep(5)  # Espera a que MongoDB inicie
    return mongodb_process

def main():
    load_dotenv()
    mongodb_process = start_mongodb()  # Inicia MongoDB
    try:
        flush_db()
        setup_db()
        randomize()
        assistant = create_character(1)
        start_screen()  # Llama a tu función de inicio de la GUI
    finally:
        # Asegúrate de cerrar MongoDB cuando la aplicación termine
        mongodb_process.terminate()
        mongodb_process.wait()

if __name__ == "__main__":
    main()
