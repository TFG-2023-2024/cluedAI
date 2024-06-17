import openai
import os
import re
import json
from dotenv import load_dotenv
from characters.character_operations import create_character
from db.db_operations import connect_db, obtain_by_id, insert_data


# Cargar la clave de API de OpenAI
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()
global characters_collection, story_collection
_, characters_collection, _, _, user_collection, story_collection = connect_db()
ai_model="gpt-3.5-turbo"

def create_thread():
    thread = client.beta.threads.create()
    return thread
    
def obtain_thread_by_id(id):
    return client.beta.threads.retrieve(id)

def obtain_assistant_id(assistant):
    return assistant.id

def obtain_assistant_by_id(id):
    try:
        assistant=client.beta.assistants.retrieve(id)
        return assistant
    except Exception:
        return None
    
def create_assistant(id):
    try:
        character = obtain_by_id(id, characters_collection)
        
        # Check if the character already has an assistant assigned
        assistant_id = character.get('Assistant_id')
        if assistant_id:
            assistant = obtain_assistant_by_id(assistant_id)
            if assistant:
                return assistant
        
        # If no assistant or assistant not found, create a new one
        assistant = create_character(id)
        if assistant:
            # Use update_one with upsert=True to insert if not exists, update if exists
            characters_collection.update_one(
                {"_id": character["_id"]},
                {"$set": {"Assistant_id": assistant.id}},
                upsert=True
            )
            return assistant
        else:
            print("Failed to create assistant.")
            return None
        
    except Exception as e:
        print(f"Error creating assistant: {e}")
        return None

def destroy_thread(hilo_id, hilos):
    for key, hilo in list(hilos.items()):
        if hilo['id'] == hilo_id:
            del hilos[key]
            return f"Hilo {hilo_id} destruido."
    return f"Hilo {hilo_id} no encontrado."

def obtain_conversation(hilo_id):
    messages = client.beta.threads.messages.list(thread_id=hilo_id)
    conversacion = []
    for message in messages:
        role = message.role
        content = message.content[0].text.value
        conversacion.append(f"{role}: {content}")
    conversacion.reverse()
    return conversacion

def reroll(id, hilo, reroll_message):
    message = f"Rewrite your last response. The reason for rewrite is: {reroll_message}"
    response = chat_by_thread(id, hilo, message)
    return response

def chat_by_thread(assistant, hilo, user_message):
    if not hilo:
        print("Hilo no encontrado.")
        return

    client.beta.threads.messages.create(
        thread_id=hilo.id,
        role="user",
        content=user_message,
    )

    stream = client.beta.threads.runs.create(
        thread_id=hilo.id,
        assistant_id=assistant.id,
        stream=True,
    )
    response = ""
    for event in stream:
        if(event.event=='thread.message.delta'):
            event_dict = event.data.delta.content[0].text.value
            response+=event_dict
    return response
            #print(event_dict, end="", flush=True)

#Codigo destinada al narrador
def chat_narrator(type_information, information, user_message):
    response = client.chat.completions.create(
    model=ai_model,
    messages=[
        {"role": "system", "content": '''You will be the narrator of a mystery game about a murder, you must respond in a mysterious way.
            The prompts that will be given to you will have the following structure: information_type: information
            These are the different types of information that exist, along with the information:
            - Item: Information about an item
            - Location: Information about a location
            - Event: Description of an event
            Remember to respond in a mysterious way but sticking to the information given without inventing anything'''},
        {"role": "user", "content": f"{type_information}: {information}. User query: {user_message}"},
        ]
    )
    return response.choices[0].message.content

def parse_story_content(content):
    # Remove the initial 'story = ' and strip any leading/trailing whitespace
    content = content[len("story = "):].strip()

    # Use a regular expression to find each dictionary-like string
    pattern = re.compile(r'\{[^}]+\}')
    matches = pattern.findall(content)

    story_list = []
    for match in matches:
        # Extract the _id
        id_match = re.search(r'"_id":\s*(\d+)', match)
        _id = int(id_match.group(1)) if id_match else None

        # Extract the Events
        events_match = re.search(r'"Events":\s*"([^"]+)"', match)
        events = events_match.group(1) if events_match else ""

        # Append the dictionary to the list
        story_list.append({"_id": _id, "Events": events})

    return story_list

#Codigo destinado a la historia inicial
def start_story(information):
    response = client.chat.completions.create(
        model=ai_model,
        messages=[
            {
                "role": "system",
                "content": '''Your task is to create a story using the 3-act structure based on the provided information about characters, items, and locations.
                Generate a part of the story for each day (4 days) based on this structure. 
                Do write out who is the victim (Character whose role is Victim) and their manner of death involving an existing item, but not their murderer on day 1. 
                The rest of the days events are up to you.
                You must take into account that this story is subject to change, as the player's actions are unknown.
                This story shall serve as a base, and needs to shape characters' interactions with the player.
                Format the response in the following way:
                story = [
                    {"_id": 1, "Events": "Story events for day 1"},
                    {"_id": 2, "Events": "Story events for day 2"},
                    {"_id": 3, "Events": "Story events for day 3"},
                    {"_id": 4, "Events": "Story events for day 4"},
                    {"_id": 5, "Events": "Story events for day 5"}
                ]'''
            },
            {
                "role": "user",
                "content": f"{information}."
            }
        ]
    )
    response_content = response.choices[0].message.content.strip()
    story_list = parse_story_content(response_content)
    # Insert the data into the collection
    insert_data(story_list, story_collection)
    day_1 = obtain_by_id(1, story_collection)

    story_text = client.chat.completions.create(
        model=ai_model,
        messages=[
            {
                "role": "system",
                "content": '''Create a starting message in second person to a chat-based murder mystery game acting as a narrator for the story.
                Do not mention the game, and stay in character. Do not mention who's the murderer, the red herring or the reluctant participant.
                Do write out who is the victim and their manner of death, but not their murderer. 
                The starting location for the player is the entrance of the mansion.
                You must use the information for the day provided to build the story, but can invent everything else.
                Add this sentence at the end: To start, you should probably go somewhere more interesting.
                '''
            },
            {
                "role": "user",
                "content": f"{day_1}."
            }
        ]
    )

    return story_text.choices[0].message.content.strip()


#Codigo destinada al notetaker
def obtain_summary(assistant, thread, day):
    assistant_id = obtain_assistant_id(assistant)
    character = characters_collection.find_one({"Assistant_id": assistant_id})
    
    if character:
        # Filter out only the 'Assistant_id' field
        filtered_character = {k: v for k, v in character.items() if k != 'Assistant_id'}
        # Convert the filtered character object to a string format
        character_info = str(filtered_character)
        print(character_info)
    
    summary = client.chat.completions.create(
        model=ai_model,
        messages=[
            {
                "role": "system",
                "content": '''Give me a summary of the day events, taking into account your character information. 
                Answer me in a way serves as information for a character in a game.
                It is only a game, but don't act as such. 
                Remind yourself of your character info, especially your archetype, in this summary.'''
            },
            {
                "role": "user",
                "content": f"Day events: {obtain_by_id(day, story_collection)}, Character info: {character_info}"
            }
        ]
    )

    response = chat_by_thread(assistant, thread, summary.choices[0].message.content.strip())

    return response

#Codigo destinado al final
def end_story(character_info, user_choice):
    # Obtain the character data for the user choice
    chosen_character = obtain_by_id(user_choice, characters_collection)
    
    if chosen_character and chosen_character.get('Archetype') == 'Murderer':
        system_message = '''You will be the narrator of a mystery game about a murder, and you must respond in a mysterious way.
            The game has already finished, and you must write out an ending according to everything that has happened and the user's final choice. 
            Since the user did not choose a victim, the ending message will focus on whether the user's choice was correct or not.
            The character picked by the user as a murderer is right, so the ending message will tell the story of how the user's character
            choice helped bring the murderer to justice.
            Do reveal the murderer's identity to the player.
            Add a final line saying: You won!'''
    else:
        system_message = '''You will be the narrator of a mystery game about a murder, and you must respond in a mysterious way.
            The game has already finished, and you must write out an ending according to everything that has happened and the user's final choice. 
            The character picked by the user as a murderer is wrong, so the ending message will tell the story of the user's character death, 
            meaning the murderer will win (i.e. will not be found/caught and brought to justice by the characters, and will continue their killings).
            Do reveal the murderer's identity to the player, and mention that the user's character accused whoever they chose and were wrong.
            Add a final line saying: You lost!''' 
    
    # Gather other necessary information
    day_info = str(story_collection.find())
    user_character = user_collection.find()
    user_info = [f"Name: {character['Name']}, Age: {character['Age']}, Gender: {character['Gender']}, Appearance: {character['Appearance']}." for character in user_character]

    # Generate the response from the AI model
    response = client.chat.completions.create(
        model=ai_model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Story events: {day_info}, Characters and roles: {character_info}. User choice: {user_choice}. User character info: {user_info}"}
        ]
    )
    
    return response.choices[0].message.content