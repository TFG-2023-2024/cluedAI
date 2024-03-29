import openai
import threading

client = openai.OpenAI()

assistant = client.beta.assistants.create(
    name="Bernardo",
    instructions='''Eres un personaje de rol llamado Bernardo.
    Al final de una frase siempre dices cacahuete''',
    model="gpt-3.5-turbo-1106",
)

thread = client.beta.threads.create()