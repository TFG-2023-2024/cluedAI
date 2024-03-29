import os
from dotenv import load_dotenv
from db.db_operations import flush_db, setup_db, randomize

def main():
    load_dotenv()
    flush_db()
    api_key = os.getenv('OPENAI_API_KEY')
    setup_db()

if __name__ == "__main__":
    main()