import openai
import os
from dotenv import load_dotenv
import random

from characters.character_operations import create_character


# Cargar la clave de API de OpenAI
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

def create_assistant(id):
    assistant = create_character(id)
    return assistant

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
    return client.beta.assistants.retrieve(id)

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
    model="gpt-3.5-turbo",
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

#Codigo destinada al notetaker
def obtain_summary(hilo_id):
    instruction = '''Give me a summary of what you consider most important of what we talked about. Answer me in a way that what you say serves as information for a person.
        As an example, if you talked about being accused of murder and you had a fight with Manuel, you should respond in the following way: You had a fight with Manuel because he accused you of murder and it made you feel bad.'''
    response = chat_by_thread(hilo_id,instruction)

    return response

#Codigo para comprobar su correcto funcionamiento
def main():
    asistete_p=obtein_assistant_by_id('asst_5ZsiYyl9Wosdk7saNjIUddzM')
    print(asistete_p)
    hilo_prueba=client.beta.threads.retrieve("thread_h7z1eu5lFk5r4LpNOTk2L4e2")
    print(hilo_prueba)
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

