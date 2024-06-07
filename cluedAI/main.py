import os
from dotenv import load_dotenv
from db.db_operations import flush_db, setup_db, randomize, start_day
from characters.character_operations import create_character
from initial_gui.start_screen import start

def main():
    
    day = 0
    load_dotenv()
    flush_db()
    api_key = os.getenv('OPENAI_API_KEY')
    setup_db()
    start_day()
    start()
    #assistant = create_character(1)

if __name__ == "__main__":
    main()