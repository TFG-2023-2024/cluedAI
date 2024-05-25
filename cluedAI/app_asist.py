#Este codigo es para probar los metodos dentro del mismo permitiendo crear x hilos con x personajes de la db mediante un rango de id ademas de acceder a dichos hilos en cualquier momento
import openai
import tkinter as tk
from dotenv import load_dotenv
import os
import threading
import random
from characters.character_operations import create_character

# Cargar la clave de API de OpenAI
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

def crear_hilos_asistentes(num_hilos, rango_ids):
    random.shuffle(rango_ids)
    ids_seleccionados = rango_ids[:num_hilos]
    asistentes = [create_character(id) for id in ids_seleccionados]
    threads = [client.beta.threads.create() for _ in range(num_hilos)]
    return asistentes, threads

def manejar_entrada(index, textos_entrada, textos_respuesta, threads, asistentes):
    entrada_usuario = textos_entrada[index].get("1.0", "end-1c")
    textos_entrada[index].delete("1.0", "end")
    textos_respuesta[index].insert(tk.END, "User: " + entrada_usuario + "\n\n")

    def consulta_api():
        message = client.beta.threads.messages.create(
            thread_id=threads[index].id,
            role="user",
            content=entrada_usuario,
        )
        run = client.beta.threads.runs.create(
            thread_id=threads[index].id,
            assistant_id=asistentes[index].id,
        )

        while True:
            run = client.beta.threads.runs.retrieve(thread_id=threads[index].id, run_id=run.id)
            if run.status == "completed":
                messages = list(client.beta.threads.messages.list(thread_id=threads[index].id))
                for message in messages:
                    if message.content[0].type == "text":
                        respuesta = message.content[0].text.value
                        textos_respuesta[index].insert(tk.END, "Asistente: " + respuesta + "\n\n")
                        break
                break

    hilo_consulta = threading.Thread(target=consulta_api)
    hilo_consulta.start()

def on_close_window(window, window_list, index):
    window_list[index] = None
    window.destroy()

def crear_ventana_entrada(index, threads, asistentes, ventanas_entrada, ventanas_salida, textos_entrada, textos_respuesta):
    if ventanas_entrada[index] is None or not ventanas_entrada[index].winfo_exists():
        ventana_entrada = tk.Toplevel()
        ventana_entrada.title(f"Input for Thread {index + 1}")
        ventana_entrada.protocol("WM_DELETE_WINDOW", lambda: on_close_window(ventana_entrada, ventanas_entrada, index))

        texto_entrada = tk.Text(ventana_entrada, height=5)
        texto_entrada.pack(fill=tk.BOTH, expand=True)
        textos_entrada[index] = texto_entrada

        boton_submit = tk.Button(ventana_entrada, text="Submit", command=lambda: crear_ventana_salida(index, threads, asistentes, ventanas_salida, textos_entrada, textos_respuesta))
        boton_submit.pack()

        ventanas_entrada[index] = ventana_entrada
    else:
        ventanas_entrada[index].deiconify()

def crear_ventana_salida(index, threads, asistentes, ventanas_salida, textos_entrada, textos_respuesta):
    if ventanas_salida[index] is None or not ventanas_salida[index].winfo_exists():
        ventana_salida = tk.Toplevel()
        ventana_salida.title(f"Output for Thread {index + 1}")
        ventana_salida.protocol("WM_DELETE_WINDOW", lambda: on_close_window(ventana_salida, ventanas_salida, index))

        texto_respuesta = tk.Text(ventana_salida, height=20)
        texto_respuesta.pack(fill=tk.BOTH, expand=True)
        textos_respuesta[index] = texto_respuesta

        ventanas_salida[index] = ventana_salida
    else:
        ventanas_salida[index].deiconify()

    manejar_entrada(index, textos_entrada, textos_respuesta, threads, asistentes)

def crear_botones_hilos(ventana_principal, num_hilos, threads, asistentes, ventanas_entrada, ventanas_salida, textos_entrada, textos_respuesta):
    for i in range(num_hilos):
        boton_hilo = tk.Button(ventana_principal, text=f"Thread {i + 1}", command=lambda i=i: crear_ventana_entrada(i, threads, asistentes, ventanas_entrada, ventanas_salida, textos_entrada, textos_respuesta))
        boton_hilo.pack(fill=tk.BOTH, expand=True)

def iniciar_aplicacion(num_hilos, rango_ids):
    ventana_principal = tk.Tk()
    ventana_principal.title("cluedAI")

    asistentes, threads = crear_hilos_asistentes(num_hilos, rango_ids)

    textos_entrada = [None] * num_hilos
    textos_respuesta = [None] * num_hilos
    ventanas_entrada = [None] * num_hilos
    ventanas_salida = [None] * num_hilos

    crear_botones_hilos(ventana_principal, num_hilos, threads, asistentes, ventanas_entrada, ventanas_salida, textos_entrada, textos_respuesta)

    ventana_principal.mainloop()

# Número de hilos y rango de IDs de personajes disponibles
NUM_HILOS = 5
RANGO_IDS = list(range(1, 11))

# Iniciar la aplicación
iniciar_aplicacion(NUM_HILOS, RANGO_IDS)
