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































# def crear_hilos_asistentes(num_hilos, rango_ids):
#     random.shuffle(rango_ids)
#     ids_seleccionados = rango_ids[:num_hilos]
#     asistentes = [create_character(id) for id in ids_seleccionados]
#     threads = [client.beta.threads.create() for _ in range(num_hilos)]
#     return asistentes, threads

# def consulta_api(index, entrada_usuario, textos_respuesta, threads, asistentes):
#     thread_id = threads[index]['id']
#     assistant_id = asistentes[index]['id']

#     mensajes = [{"role": "user", "content": entrada_usuario}]

#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=mensajes,
#         stream=True  # Habilitar el streaming
#     )

#     # Limpiar el campo de respuesta antes de comenzar a recibir la nueva respuesta
#     textos_respuesta[index].delete("1.0", tk.END)
#     respuesta_completa = ""

#     for chunk in response:
#         if 'choices' in chunk:
#             for choice in chunk['choices']:
#                 if 'delta' in choice and 'content' in choice['delta']:
#                     texto_parcial = choice['delta']['content']
#                     respuesta_completa += texto_parcial
#                     textos_respuesta[index].insert(tk.END, texto_parcial)
#                     textos_respuesta[index].see(tk.END)  # Scroll al final para ver la nueva respuesta

#     return respuesta_completa

# def manejar_entrada(index, textos_entrada, textos_respuesta, threads, asistentes):
#     entrada_usuario = textos_entrada[index].get("1.0", "end-1c")
#     textos_entrada[index].delete("1.0", "end")
#     textos_respuesta[index].insert(tk.END, "User: " + entrada_usuario + "\n\n")

#     hilo_consulta = threading.Thread(target=consulta_api, args=(index, entrada_usuario, textos_respuesta, threads, asistentes))
#     hilo_consulta.start()

# def on_close_window(window, window_list, index):
#     window_list[index] = None
#     window.destroy()

# def crear_ventana_entrada(index, threads, asistentes, ventanas_entrada, ventanas_salida, textos_entrada, textos_respuesta):
#     if ventanas_entrada[index] is None or not ventanas_entrada[index].winfo_exists():
#         ventana_entrada = tk.Toplevel()
#         ventana_entrada.title(f"Input for Thread {index + 1}")
#         ventana_entrada.protocol("WM_DELETE_WINDOW", lambda: on_close_window(ventana_entrada, ventanas_entrada, index))

#         texto_entrada = tk.Text(ventana_entrada, height=5)
#         texto_entrada.pack(fill=tk.BOTH, expand=True)
#         textos_entrada[index] = texto_entrada

#         boton_submit = tk.Button(ventana_entrada, text="Submit", command=lambda: crear_ventana_salida(index, threads, asistentes, ventanas_salida, textos_entrada, textos_respuesta))
#         boton_submit.pack()

#         ventanas_entrada[index] = ventana_entrada
#     else:
#         ventanas_entrada[index].deiconify()

# def crear_ventana_salida(index, threads, asistentes, ventanas_salida, textos_entrada, textos_respuesta):
#     if ventanas_salida[index] is None or not ventanas_salida[index].winfo_exists():
#         ventana_salida = tk.Toplevel()
#         ventana_salida.title(f"Output for Thread {index + 1}")
#         ventana_salida.protocol("WM_DELETE_WINDOW", lambda: on_close_window(ventana_salida, ventanas_salida, index))

#         texto_respuesta = tk.Text(ventana_salida, height=20)
#         texto_respuesta.pack(fill=tk.BOTH, expand=True)
#         textos_respuesta[index] = texto_respuesta

#         ventanas_salida[index] = ventana_salida
#     else:
#         ventanas_salida[index].deiconify()

#     manejar_entrada(index, textos_entrada, textos_respuesta, threads, asistentes)

# def crear_botones_hilos(ventana_principal, num_hilos, threads, asistentes, ventanas_entrada, ventanas_salida, textos_entrada, textos_respuesta):
#     for i in range(num_hilos):
#         boton_hilo = tk.Button(ventana_principal, text=f"Thread {i + 1}", command=lambda i=i: crear_ventana_entrada(i, threads, asistentes, ventanas_entrada, ventanas_salida, textos_entrada, textos_respuesta))
#         boton_hilo.pack(fill=tk.BOTH, expand=True)

# def iniciar_aplicacion(num_hilos, rango_ids):
#     ventana_principal = tk.Tk()
#     ventana_principal.title("cluedAI")

#     asistentes, threads = crear_hilos_asistentes(num_hilos, rango_ids)

#     textos_entrada = [None] * num_hilos
#     textos_respuesta = [None] * num_hilos
#     ventanas_entrada = [None] * num_hilos
#     ventanas_salida = [None] * num_hilos

#     crear_botones_hilos(ventana_principal, num_hilos, threads, asistentes, ventanas_entrada, ventanas_salida, textos_entrada, textos_respuesta)

#     ventana_principal.mainloop()

# # Número de hilos y rango de IDs de personajes disponibles
# NUM_HILOS = 5
# RANGO_IDS = list(range(1, 11))

# # Iniciar la aplicación
# iniciar_aplicacion(NUM_HILOS, RANGO_IDS)
