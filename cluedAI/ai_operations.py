import openai
import os
from dotenv import load_dotenv
from characters.character_operations import create_character

# Cargar la clave de API de OpenAI
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

def crear_asistente(id):
    assistant = create_character(id)
    return assistant

def crear_hilo():
    thread = client.beta.threads.create()
    return {"id": thread.id}

def obtener_id_hilo(hilo):
    return hilo['id']

def destruir_hilo(hilo_id, hilos):
    for key, hilo in list(hilos.items()):
        if hilo['id'] == hilo_id:
            del hilos[key]
            return f"Hilo {hilo_id} destruido."
    return f"Hilo {hilo_id} no encontrado."

def recuperar_conversacion(hilo_id):
    messages = client.beta.threads.messages.list(thread_id=hilo_id)
    conversacion = []
    for message in messages:
        role = message.role
        content = message.content[0].text.value
        conversacion.append(f"{role.capitalize()}: {content}")
    return conversacion

def reroll(hilo, reroll_message):
    message = f"Rewrite your last response. The reason for rewrite is: {reroll_message}"
    response = conversar_en_hilo(hilo, message)
    return response

def conversar_en_hilo(hilo, user_message):
    if not hilo:
        print("Hilo no encontrado.")
        return

    asistente = crear_asistente(1)
    print(asistente)

    client.beta.threads.messages.create(
        thread_id=hilo['id'],
        role="user",
        content=user_message,
    )

    stream = client.beta.threads.runs.create(
        thread_id=hilo['id'],
        assistant_id=asistente.id,
        stream=True,
    )
    response = ""
    for event in stream:
        if(event.event=='thread.message.delta'):
            event_dict = event.data.delta.content[0].text.value
            response+=event_dict
    return response