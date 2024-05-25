from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/aya/Documents/tfg/cluedAI/build/assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1024x768")

def handle_message():
    pass

canvas = Canvas(
    window,
    bg = "#202020",
    height = 768,
    width = 1024,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    515.0,
    403.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    512.0,
    699.0,
    image=image_image_2
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=925.66845703125,
    y=672.6683959960938,
    width=54.33160400390625,
    height=54.33160400390625
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    461.0,
    698.5,
    image=entry_image_1
)

def clear_default(event):
    event.widget.delete(0, 'end')
    event.widget.unbind('<FocusIn>')

entry_reply = Entry(
    bd=0,
    bg="#1F1F1F",
    fg="#FFFFFF",
    highlightthickness=0
)

entry_reply.insert(0, "Write your response here...")  # Insert default text
entry_reply.bind('<FocusIn>', clear_default)
entry_reply.bind("<Return>", handle_message)

entry_reply.place(
    x=56.0,
    y=673.0,
    width=810.0,
    height=49.0
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    511.0,
    42.0,
    image=image_image_3
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=291.66650390625,
    y=30.0,
    width=26.66666603088379,
    height=20.0
)

# Create the "clued" text
clued_text = canvas.create_text(
    454.0,
    22.0,
    anchor="nw",
    text="Clued",
    fill="#F4F4F4",
    font=("Inter", 30 * -1)
)

# Calculate the width of the "clued" text
clued_bbox = canvas.bbox(clued_text)
clued_width = clued_bbox[2] - clued_bbox[0]

# Create the "AI" text
canvas.create_text(
    454.0 + clued_width,  # Adjust x-coordinate to center "AI" text relative to "clued" text
    22.0,
    anchor="nw",
    text="AI",
    fill="#D71E1E",
    font=("Inter", 30 * -1)
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=696.0,
    y=24.0,
    width=34.0,
    height=32.0
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    248.0,
    209.0,
    image=image_image_4
)

canvas.create_text(
    74.0,
    161.0,
    anchor="nw",
    text="I am ChatGPT, a conversational AI language model developed by OpenAI. I am designed to process natural language and respond to various queries and conversations in a way that simulates human-like conversation. My purpose is to assist and provide helpful responses to users who interact with me.",
    fill="#FFFFFF",
    font=("Inter", 13 * -1)
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    916.0,
    360.0,
    image=image_image_5
)

canvas.create_text(
    872.0,
    352.0,
    anchor="nw",
    text="how are you?",
    fill="#FFFFFF",
    font=("Inter", 13 * -1)
)
window.resizable(False, False)
window.mainloop()
