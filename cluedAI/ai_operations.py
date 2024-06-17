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
_, characters_collection, _, _, _, story_collection = connect_db()
ai_model="gpt-3.5-turbo"

def create_thread():
    thread = client.beta.threads.create()
    return thread
    
def obtain_thread_by_id(id):
    try:
        return client.beta.threads.retrieve(id)
    except Exception:
        return None
    

def obtain_assistant_id(assistant):
    return assistant.id

def obtein_assistant_by_id(id):
    try:
        assistant=client.beta.assistants.retrieve(id)
        return assistant
    except Exception:
        return None
    
def create_assistant(id):
    character = obtain_by_id(id, characters_collection)
    assistant=obtein_assistant_by_id(character['Assistant_id'])
    if(assistant):
        return assistant
    else:
        assistant = create_character(id)
        characters_collection.update_one(
                {"_id": character["_id"]},
                {"$set": {"Assistant_id": assistant.id}})
        return assistant

def destroy_thread(id):
    try:
        return client.beta.threads.delete(id)
    except Exception:
        return None

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


#Codigo destinada a renovar la información del asistente en un hilo nuevo
def obtain_summary(assistant, thread_to_summary, new_thread, day):
    if day !=1:
        conversacion= obtain_conversation(thread_to_summary.id)
        instruction_summary = f'''Give me a summary of what you consider most important of what was talked about in this conversation: {conversacion}
        In the conversation you are the assistant and I am the user
        It is only a game, but don't act as such.
        Respond to me in the second person, for example, instead of saying I come from, you should respond as you come from.'''

        summary_thread=chat_by_thread(assistant, thread_to_summary, instruction_summary)
        destroy_thread(thread_to_summary.id)
        instruction_to_new_thread=f'''This is information about what happened the last time we spoke,
          keep in mind that this information is from your point of view, that is, as if you were answering yourself.:
        {summary_thread}'''
        chat_by_thread(assistant, new_thread, instruction_to_new_thread)
        conversacion2= obtain_conversation(new_thread.id)
        return summary_thread

