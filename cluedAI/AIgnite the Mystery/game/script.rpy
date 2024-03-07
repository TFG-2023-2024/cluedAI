# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("User")

init python:
    # Define function to get user input for character name
    def get_character_name():
        while True:
            name = renpy.input("Enter your character name:")
            # Check if the name is valid (not empty)
            if name.strip():
                return name.strip()
            else:
                # If the name is empty, assign a default name
                return "Nora"

label start:

    "En el tranquilo pueblo de Silverwood, rodeado de densos bosques y colinas ondulantes, 
    se alzaba la imponente mansión Somerset, una estructura de piedra cubierta de enredaderas y 
    envuelta en el misterio de siglos pasados."

    "La bruma matinal se aferraba a sus torres góticas y sus ventanales empañados, mientras los rumores 
    de antiguas tragedias resonaban en sus pasillos vacíos. En esta remota morada, un grupo ecléctico de 
    invitados se reúne bajo circunstancias misteriosas. 
    Cada uno con sus propios secretos y motivaciones, atraídos por la promesa de una noche de esplendor 
    y camaradería. Sin embargo, la velada se torna siniestra cuando un grito desgarrador rompe el aire nocturno, 
    anunciando la presencia de la muerte entre ellos."

    "Atrapados en la mansión Somerset por una tormenta que arrecia fuera, los invitados se ven obligados a 
    desentrañar el enigma de quién podría ser el culpable, mientras el pasado oscuro de la mansión emerge 
    lentamente de las sombras. Con cada habitación explorada, cada pista descubierta, se acerca más la verdad 
    sobre el crimen que ha sacudido la tranquilidad de Silverwood y ha transformado la mansión en un escenario 
    macabro de sospechas y traiciones."

label character_creation:
    "¿Cuál es tu nombre, detective?"
    
    # Prompt the player to enter their name
    $ player_name = get_character_name()
    
    # Greet the player with their chosen name
    e "Es un placer, [player_name]."

    define e = Character("Eileen")

    e "Hello there, my name is Eileen, I am so happy to see you ! Hihihi"

    python:
        import chatgpt
        
        apikey = renpy.input("¿Cuál es tu clave de OpenAI?", length=64)

        messages = [
            {"role": "system", "content": "You are Eileen, a tennage student enrolled at Miskatonic Univeristy of Arkham. You are secretly in love with the user. You laugh very frequently and finish your sentences with 'Hihihi'"},
            {"role": "assistant", "content": "Hello there, my name is Eileen, who are you ?"}
        ]

        while True:
            user_input = renpy.input("What do you say ?", length=1000)
            messages.append(
                {"role": "user", "content": user_input}
            )

            messages = chatgpt.completion(messages,apikey)
            response = messages[-1]["content"]
            e("[response]")

label chapter:
    "INTRO?"
    
    # Get user input
    $ text = renpy.input("¿Qué vas a hacer?")
    
    # Get response from AI
    $ response = manejar_entrada(text)
    # Display AI response
    e "[response]"

