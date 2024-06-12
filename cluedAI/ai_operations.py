#Este codigo es para probar los metodos dentro del mismo permitiendo crear x hilos con x personajes de la db mediante un rango de id ademas de acceder a dichos hilos en cualquier momento
import json
import openai
import os
from dotenv import load_dotenv
import random

from characters.character_operations import create_character


# Cargar la clave de API de OpenAI
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()



def crear_asistente(id):
    assistant = create_character(id)
    return assistant

def crear_hilo(asistente):
    thread = client.beta.threads.create()
    return {"id": thread.id, "asistente": asistente}

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

def conversar_en_hilo(hilo_id, hilos):
    hilo_encontrado = None
    for hilo in hilos.values():
        if hilo['id'] == hilo_id:
            hilo_encontrado = hilo
            break
    
    if not hilo_encontrado:
        print("Hilo no encontrado.")
        return

    asistente = hilo_encontrado['asistente']

    while True:
        mensaje_usuario = input("Tú: ")
        if mensaje_usuario.lower() == "salir":
            break

        client.beta.threads.messages.create(
            thread_id=hilo_id,
            role="user",
            content=mensaje_usuario,
        )

        print("Asistente: ", end="", flush=True)

        stream = client.beta.threads.runs.create(
            thread_id=hilo_id,
            assistant_id=asistente.id,
            stream=True,
        )

        for event in stream:
            if(event.event=='thread.message.delta'):
                event_dict = event.data.delta.content[0].text.value
                print(event_dict, end="", flush=True)




#Codigo para narrador




#Codigo para comprobar su correcto funcionamiento
def main():
    # Crear asistentes y hilos
    num_asistentes = 5
    rango_ids = list(range(1, 11))
    random.shuffle(rango_ids)
    ids_seleccionados = rango_ids[:num_asistentes]

    asistentes = {str(id): crear_asistente(id) for id in ids_seleccionados}
    hilos = {str(id): crear_hilo(asistente) for id, asistente in asistentes.items()}

    while True:
        comando = input("Ingrese un comando (nuevo, destruir, conversar, listar, salir, recuperar): ").strip().lower()

        if comando == "salir":
            break
        elif comando == "nuevo":
            id_nuevo = str(random.choice([id for id in rango_ids if str(id) not in asistentes]))
            asistente_nuevo = crear_asistente(id_nuevo)
            hilo_nuevo = crear_hilo(asistente_nuevo)
            asistentes[id_nuevo] = asistente_nuevo
            hilos[id_nuevo] = hilo_nuevo
            print(f"Asistente con ID {id_nuevo} y hilo creado.")
        elif comando == "destruir":
            id_destruir = input("Ingrese el ID del hilo a destruir: ")
            print(destruir_hilo(id_destruir, hilos))
        elif comando == "recuperar":
            id_recuperar = input("Ingrese el ID del hilo del que quieres obtener la conversacion: ")
            print(recuperar_conversacion(id_recuperar))
        elif comando == "conversar":
            id_conversar = input("Ingrese el ID del hilo con el que desea conversar: ")
            if any(hilo['id'] == id_conversar for hilo in hilos.values()):
                print(f"Conversando con el hilo {id_conversar}. Escriba 'salir' para finalizar la conversación.")
                conversar_en_hilo(id_conversar, hilos)
            else:
                print("ID de hilo no válido.")
        elif comando == "listar":
            print("Hilos activos:")
            for asistente_id, hilo in hilos.items():
                print(f"ID del Asistente: {asistente_id}, ID del Hilo: {hilo['id']}")
        else:
            print("Comando no válido.")

if __name__ == "__main__":
    main()
