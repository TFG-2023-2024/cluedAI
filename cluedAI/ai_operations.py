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
    return {"id": thread.id}

def obtain_thread_id(hilo):
    return hilo['id']
    
def obtain_thread_by_id(id):
    return client.beta.threads.retrieve(id)

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
        thread_id=hilo['id'],
        role="user",
        content=user_message,
    )

    stream = client.beta.threads.runs.create(
        thread_id=hilo['id'],
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
                Generate a part of the story for each day (7 days) based on this structure. 
                You must take into account that this story is subject to change, as the player's actions are unknown.
                This story shall serve as a base, and needs to shape characters' interactions with the player.
                Format the response in the following way:
                story = [
                    {"_id": 1, "Events": "Story events for day 1"},
                    {"_id": 2, "Events": "Story events for day 2"},
                    {"_id": 3, "Events": "Story events for day 3"},
                    {"_id": 4, "Events": "Story events for day 4"},
                    {"_id": 5, "Events": "Story events for day 5"},
                    {"_id": 6, "Events": "Story events for day 6"},
                    {"_id": 7, "Events": "Story events for day 7"}
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
                Do not mention the game, and stay in character. Do not mention who's the murderer or red herring. 
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
def obtain_summary(assistant, hilo):
    instruction = '''Give me a summary of what you consider most important of what we talked about. Answer me in a way that what you say serves as information for a person.
        As an example, if you talked about being accused of murder and you had a fight with Manuel, you should respond in the following way: You had a fight with Manuel because he accused you of murder and it made you feel bad.'''
    response = chat_by_thread(assistant, hilo,instruction)

    return response

'''
#Codigo para comprobar su correcto funcionamiento
def main():
    asistete_p=create_assistant(1)
    print(asistete_p)
    # hilo_prueba=client.beta.threads.retrieve("thread_h7z1eu5lFk5r4LpNOTk2L4e2")
    # print(hilo_prueba)
    # num_asistentes = 5
    #rango_ids = list(range(1, 11))
    # random.shuffle(rango_ids)
    # ids_seleccionados = rango_ids[:num_asistentes]

    # asistentes = {str(id): create_assistant(id) for id in rango_ids}
    # print(asistentes)
    # hilos = {str(id): create_thread() for id, asistente in asistentes.items()}

    # while True:
    #     comando = input("Ingrese un comando (nuevo, destruir, conversar, listar, salir, recuperar): ").strip().lower()

    #     if comando == "salir":
    #         break
    #     elif comando == "nuevo":
    #         id_nuevo = str(random.choice([id for id in rango_ids if str(id) not in asistentes]))
    #         asistente_nuevo = create_assistant(id_nuevo)
    #         hilo_nuevo = create_thread(asistente_nuevo)
    #         asistentes[id_nuevo] = asistente_nuevo
    #         hilos[id_nuevo] = hilo_nuevo
    #         print(f"Asistente con ID {id_nuevo} y hilo creado.")
    #     elif comando == "destruir":
    #         id_destruir = input("Ingrese el ID del hilo a destruir: ")
    #         print(destroy_thread(id_destruir, hilos))
    #     elif comando == "recuperar":
    #         id_recuperar = input("Ingrese el ID del hilo del que quieres obtener la conversacion: ")
    #         print(obtain_conversation(id_recuperar))
    #     elif comando == "resumen":
    #         id_resumir = input("Ingrese el ID del hilo del que quieres obtener el resumen: ")
    #         print(obtain_summary(id_resumir))
    #     elif comando == "conversar":
    #         id_conversar = input("Ingrese el ID del hilo con el que desea conversar: ")
    #         asistente_nuevo = create_assistant(2)
    #         if any(hilo['id'] == id_conversar for hilo in hilos.values()):
    #             msg = input("msg: ")
    #             print(chat_by_thread(asistente_nuevo,hilo, msg))
    #         else:
    #             print("ID de hilo no válido.")
    #     elif comando == "listar":
    #         print("Hilos activos:")
    #         for asistente_id, hilo in hilos.items():
    #             print(f"ID del Asistente: {asistente_id}, ID del Hilo: {hilo['id']}")
    #     else:
    #         print("Comando no válido.")

if __name__ == "__main__":
    main()
'''