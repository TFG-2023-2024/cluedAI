import openai
import tkinter as tk
from dotenv import load_dotenv
import os
import threading

# Cargar y configurar la API de OpenAI
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

assistant = client.beta.assistants.create(
    name="Bernardo",
    instructions='''Eres un personaje de rol llamado Bernardo.
    Al final de una frase siempre dices cacahuete''',
    model="gpt-3.5-turbo-1106",
)
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
                    texto_respuesta.insert(tk.END, "Asistente: " + respuesta + "\n\n")
                    break
                break


    hilo_consulta = threading.Thread(target=consulta_api)
    hilo_consulta.start()



# Configuración de la ventana Tkinter
ventana = tk.Tk()
ventana.title("Asistente Gracioso")

# Etiqueta para el campo de texto de entrada
etiqueta_entrada = tk.Label(ventana, text="Conversación:")
etiqueta_entrada.pack()

# Área de texto para mostrar respuestas
texto_respuesta = tk.Text(ventana, height=20)
texto_respuesta.pack(fill=tk.BOTH, expand=True)

# Etiqueta para el campo de texto de entrada
etiqueta_entrada = tk.Label(ventana, text="Escribe aqui:")
etiqueta_entrada.pack()

# Campo de texto para la entrada del usuario
texto_entrada = tk.Text(ventana, height=5)
texto_entrada.pack(fill=tk.BOTH, expand=True)

# Botón para enviar texto
boton_enviar = tk.Button(ventana, text="Enviar", command=manejar_entrada)
boton_enviar.pack(side=tk.BOTTOM)

# Vincula la tecla Enter para poder enviar sin pulsar el boton
texto_entrada.bind("<Return>", manejar_entrada)

# Iniciar la interfaz gráfica
ventana.mainloop()
