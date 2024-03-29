import os
from dotenv import load_dotenv
from db.db_operations import flush_db, setup_db, randomize, connect_db

def main():
    load_dotenv()
    flush_db()
    api_key = os.getenv('OPENAI_API_KEY')
    setup_db()
    randomize()

if __name__ == "__main__":
    main()