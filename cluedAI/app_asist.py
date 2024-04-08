import openai
import tkinter as tk
from dotenv import load_dotenv
import os
import threading
from db.db_operations import connect_db, obtain_by_id
from characters.character_operations import create_character

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
print(os.getenv('OPENAI_API_KEY'))
client = openai.OpenAI()
assistant = create_character(1)
thread = client.beta.threads.create()

# Función para manejar la entrada del usuario y obtener la respuesta de OpenAI
def manejar_entrada(event=None):
    entrada_usuario = texto_entrada.get("1.0", "end-1c")
    texto_entrada.delete("1.0", "end")
    texto_respuesta.insert(tk.END, "User: " + entrada_usuario + "\n\n")

    def consulta_api():
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=entrada_usuario,
        )
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        while True:
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run.status == "completed":
                messages = list(client.beta.threads.messages.list(thread_id=thread.id))
                for message in messages:
                    assert message.content[0].type == "text"
                    respuesta = message.content[0].text.value
                    print(respuesta)
                    texto_respuesta.insert(tk.END, "Asistente: " + respuesta + "\n\n")
                    break
                break


    hilo_consulta = threading.Thread(target=consulta_api)
    hilo_consulta.start()

# Función para mostrar los registros completos de la conversación
def show_logs():
    # Aquí iría la lógica para mostrar los registros completos de la conversación
    pass

# Function to change the button appearance when clicked
def animate_button_click(button):
    # Change button background color when clicked
    button.config(bg="red")
    # Change button relief to SUNKEN
    button.config(relief=tk.SUNKEN)
    # After a delay, change button back to normal appearance
    button.after(200, lambda: restore_button(button))

# Function to restore the button appearance
def restore_button(button):
    # Restore button background color
    button.config(bg="SystemButtonFace")
    # Restore button relief to RAISED
    button.config(relief=tk.RAISED)

# Configuración de la ventana Tkinter
ventana = tk.Tk()
ventana.title("cluedAI")

# Etiqueta para el campo de texto de entrada
etiqueta_entrada = tk.Label(ventana, text="Conversation:")
etiqueta_entrada.pack()

# Área de texto para mostrar respuestas
texto_respuesta = tk.Text(ventana, height=20)
texto_respuesta.pack(fill=tk.BOTH, expand=True)

# Etiqueta para el campo de texto de entrada
etiqueta_entrada = tk.Label(ventana, text="Write here:")
etiqueta_entrada.pack()

# Campo de texto para la entrada del usuario
texto_entrada = tk.Text(ventana, height=5)
texto_entrada.pack(fill=tk.BOTH, expand=True)

# Botón para enviar texto
boton_enviar = tk.Button(ventana, text="Send", command=manejar_entrada)
boton_enviar.pack(side=tk.BOTTOM)
boton_enviar.bind("<Button-1>", lambda event: animate_button_click(boton_enviar))

# Botón para ver registros completos de la conversación
boton_logs = tk.Button(ventana, text="Logs", command=show_logs)
boton_logs.pack(side=tk.BOTTOM)

# Vincula la tecla Enter para poder enviar sin pulsar el boton
texto_entrada.bind("<Return>", manejar_entrada)

# Iniciar la interfaz gráfica
ventana.mainloop()
