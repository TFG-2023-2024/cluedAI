import os
from dotenv import load_dotenv
from db.db_operations import flush_db, setup_db, randomize
from characters.character_operations import create_character
from initial_gui import start_screen

def main():
    
   """  load_dotenv()
    flush_db()
    api_key = os.getenv('OPENAI_API_KEY')
    setup_db()
    randomize()
    assistant = create_character(1) """



if __name__ == "__main__":
    main()