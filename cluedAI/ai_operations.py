import openai
import os
import re
from dotenv import load_dotenv
from characters.character_operations import create_character
from db.db_operations import connect_db, obtain_by_id, insert_data

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()
global characters_collection, story_collection
_, characters_collection, _, _, user_collection, story_collection = connect_db()
ai_model="gpt-3.5-turbo"

def create_thread():
    """
    Create a new thread using the client's beta API.

    This function calls the client's method to create a new thread.

    Returns:
    - thread (object): The created thread object.
    """
    thread = client.beta.threads.create()
    return thread
    
def obtain_thread_by_id(id):
    """
    Retrieve a thread by its ID using the client's beta API.

    This function attempts to retrieve a thread by its ID.

    Args:
    - id (str): The ID of the thread to retrieve.

    Returns:
    - thread (object or None): The retrieved thread object, or None if not found.
    """
    try:
        return client.beta.threads.retrieve(id)
    except Exception:
        return None
    

def obtain_assistant_id(assistant):
    """
    Retrieve the ID of an assistant object.

    This function returns the ID of the provided assistant object.

    Args:
    - assistant (object): The assistant object.

    Returns:
    - id (str): The ID of the assistant.
    """
    return assistant.id

def obtain_assistant_by_id(id):
    """
    Retrieve an assistant by its ID using the client's beta API.

    This function attempts to retrieve an assistant by its ID.

    Args:
    - id (str): The ID of the assistant to retrieve.

    Returns:
    - assistant (object or None): The retrieved assistant object, or None if not found.
    """
    try:
        assistant=client.beta.assistants.retrieve(id)
        return assistant
    except Exception:
        return None
    
def create_assistant(id):
    """
    Create an assistant associated with a character ID.

    This function first checks if the character already has an assistant assigned.
    If not, it creates a new assistant and updates the character document in the characters_collection.

    Args:
    - id (str): The ID of the character associated with the assistant.

    Returns:
    - assistant (object or None): The created or retrieved assistant object, or None if creation failed.
    """
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

def destroy_thread(id):
    """
    Destroy (delete) a thread by its ID using the client's beta API.

    This function attempts to delete a thread by its ID.

    Args:
    - id (str): The ID of the thread to delete.

    Returns:
    - result (object or None): The result of the deletion operation, or None if deletion failed.
    """
    try:
        return client.beta.threads.delete(id)
    except Exception:
        return None

def obtain_conversation(hilo_id):
    """
    Retrieve a conversation (list of messages) from a thread by its ID using the client's beta API.

    This function retrieves messages from a thread and formats them into a conversation list.

    Args:
    - hilo_id (str): The ID of the thread to retrieve messages from.

    Returns:
    - conversacion (list): A list of formatted messages in the conversation.
    """
    messages = client.beta.threads.messages.list(thread_id=hilo_id)
    conversacion = []
    for message in messages:
        role = message.role
        content = message.content[0].text.value
        conversacion.append(f"{role}: {content}")
    conversacion.reverse()
    return conversacion

def reroll(assistant, thread, reroll_message):
    """
    Perform a reroll in a thread by sending a message and receiving a response.

    This function sends a reroll message to a thread and retrieves the response.

    Args:
    - id (str): The ID associated with the reroll operation.
    - hilo (object): The thread object where the reroll message will be sent.
    - reroll_message (str): The message explaining the reroll reason.

    Returns:
    - response (str): The response received after the reroll message is sent.
    """
    message = f"Rewrite your last response. The reason for rewrite is: {reroll_message}"
    response = chat_by_thread(assistant, thread, message)
    return response

def chat_by_thread(assistant, hilo, user_message):
    """
    Perform a chat action in a thread by sending a message and processing the response.

    This function sends a message to a thread and processes the response to build a complete message.

    Args:
    - assistant (object): The assistant object associated with the chat action.
    - hilo (object): The thread object where the message will be sent.
    - user_message (str): The message sent by the user.

    Returns:
    - response (str): The complete response received after processing the chat action.
    """
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

def chat_narrator(type_information, information, user_message):
    """
    Initiate a chat with the narrator AI for the game.

    This function sends a message to the AI model to interact as the narrator role,
    responding to user queries based on predefined information types.

    Args:
    - type_information (str): Type of information (e.g., Item, Location, Event...).
    - information (str): Specific information related to the type.
    - user_message (str): User query message.

    Returns:
    - response (str): AI-generated response in the form of a mysterious narrative.
    """
    response = client.chat.completions.create(
    model=ai_model,
    messages=[
        {"role": "system", "content": '''You will be the narrator of a mystery game about a murder, you must respond in a mysterious way.
            The prompts that will be given to you will have the following structure: information_type: information. User query: user_message.
            These are the different types of information that exist, along with the information:
            - Item: Information about an item.
            - Location: Information about a location.
            Remember to respond to the user query in a mysterious way but mostly sticking to the information given.
            '''},
        {"role": "user", "content": f"{type_information}: {information}. User query: {user_message}"},
        ]
    )
    return response.choices[0].message.content

def parse_story_content(content):
    """
    Parse and extract story events from a formatted content string.

    This function extracts story events for each day from a formatted content string
    and returns them as a list of dictionaries.

    Args:
    - content (str): Formatted content string containing story events.

    Returns:
    - story_list (list): List of dictionaries containing _id and Events for each day.
    """
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
        story_list.append({"_id": _id, "Events": events})

    return story_list

def start_story(information):
    """
    Start the creation of a story using the 3-act structure (can ve varied) based on provided information.

    This function initiates the creation of a story based on provided information,
    involving characters, items, and locations. It formats the response for each day
    and stores it in a collection for further use.

    Args:
    - information (str): Initial information to start the story.

    Returns:
    - story_text (str): AI-generated response containing the formatted story text for day 1.
    """
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

def obtain_summary(assistant, thread_to_summary, day, new_thread=None):
    """
    Obtain a summary of events and character data for a given day and thread.

    This function interacts with the AI model to obtain a summary of events for a given day
    and character information for the assistant role in a game scenario. It also handles
    thread summary and redirection if a new thread is provided.

    Args:
    - assistant (object): Assistant object associated with the game.
    - thread_to_summary (object): Thread object to summarize events.
    - day (int): Day number to fetch story events.
    - new_thread (object, optional): New thread object for redirection.
    """
    assistant_id = obtain_assistant_id(assistant)
    character = characters_collection.find_one({"Assistant_id": assistant_id})
    
    if character:
        # Filter out only the 'Assistant_id' field
        filtered_character = {k: v for k, v in character.items() if k != 'Assistant_id'}
        character_info = str(filtered_character)
    
    summary = client.chat.completions.create(
        model=ai_model,
        messages=[
            {
                "role": "system",
                "content": '''Give me a summary of the day events, taking into account your character information. 
                Answer me in a way serves as information for a character in a game.
                It is only a game, but don't act as such. 
                Remind yourself of your character info, and add your archetype in this summary.'''
            },
            {
                "role": "user",
                "content": f"Day events: {obtain_by_id(day, story_collection)}, Character info: {character_info}, Archetype: {character['Archetype']}"
            }
        ]
    )

    if day !=1 and new_thread!=None:
        conversacion= obtain_conversation(thread_to_summary.id)
        instruction_summary = f'''Give me a summary of what you consider most important of what was talked about in this conversation: {conversacion}
        In the conversation you are the assistant and I am the user.
        It is only a game, but don't act as such.
        Respond to me in the second person, for example, instead of saying I come from, you should respond as you come from.'''

        summary_thread=chat_by_thread(assistant, thread_to_summary, instruction_summary)
        destroy_thread(thread_to_summary.id)
        instruction_to_new_thread=f'''This is information about what happened the last time we spoke,
          keep in mind that this information is from your point of view, that is, as if you were answering yourself.:
        {summary_thread}'''
        print(chat_by_thread(assistant, new_thread, summary.choices[0].message.content.strip()))
        print(chat_by_thread(assistant, new_thread, instruction_to_new_thread))
    else:
        print(chat_by_thread(assistant, thread_to_summary, summary.choices[0].message.content.strip()))

def end_story(character_info, user_choice):
    """
    End the story with a final message based on the user's final choice.

    This function generates an ending message for the murder mystery game based on
    the user's final choice and character information.

    Args:
    - character_info (str): Information about characters and roles.
    - user_choice (int): User's final choice related to the murderer.

    Returns:
    - response (str): AI-generated ending message based on the game outcome.
    """
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
    
    # Gather necessary information
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