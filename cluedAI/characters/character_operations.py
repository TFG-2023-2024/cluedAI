import openai
import os
from dotenv import load_dotenv
from db.db_operations import connect_db, obtain_by_id

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

def create_character(id):
    """
    Creates an OpenAI assistant for a character fetched from the database.

    Args:
    - id (any): The ID of the character to create an assistant for.

    Returns:
    - assistant (openai.ChatCompletion): The created OpenAI assistant.
    """
    try:
        # Obtain the character from the database
        _, characters_collection, _, _, _ = connect_db()
        character = obtain_by_id(id, characters_collection)
        if character:
            # Convert the character object to a string format
            character_info = str(character)
            # Create the assistant with the character's name and roleplaying instructions
            assistant = client.beta.assistants.create(
                name=f"{character['Name']}",
                instructions=f'''You are roleplaying as {character['Name']} in a murder mystery game. 
                Follow the instructions provided by your character sheet: {character_info}''',
                model="gpt-3.5-turbo-1106",
            )
            return assistant
        else:
            print("Character not found.")
            return None
    except Exception as e:
        print(f"Error creating character assistant: {e}")
        return None