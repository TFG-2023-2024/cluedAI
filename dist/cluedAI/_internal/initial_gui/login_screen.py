from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
from dotenv import load_dotenv
from users.user_operations import log_user
from initial_gui.create_screen import create
import os

#load_dotenv()
#openai_api_key = os.getenv('OPENAI_API_KEY')

def login():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("assets/login")


    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)
    
    window = Tk()

    window.geometry("1024x768")

    def create_character():
        api = entry_key.get()
        username = entry_username.get()
        
        if not api or not username or api=="Enter your API Key" or username=="Enter your username":
            messagebox.showerror(title='Error', message='Both fields must be completed.', icon="error")
        elif api != "a":  
            messagebox.showerror(title='Error', message='The API key is incorrect.', icon="error")
        else:
            log_user(username)
            window.destroy()
            create(username)


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
    canvas.create_image(
        515.0,
        403.0,
        image=image_image_1
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        highlightthickness=0,
        command=create_character,
        relief="flat"
    )
    button_1.place(
        x=334.0,
        y=634.0,
        width=355.0,
        height=53.0
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        511.0,
        546.0,
        image=image_image_2
    )

    def clear_default(event):
        event.widget.delete(0, 'end')
        event.widget.unbind('<FocusIn>')

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        531.0,
        546.0,
        image=entry_image_1
    )

    entry_key = Entry(
        bd=0,
        bg="#292929",
        fg="#FFFFFF",
        font=("Inter", 13 * -1),
        highlightthickness=0
    )
    entry_key.insert(0, "Enter your API Key")  # Insert default text
    entry_key.bind('<FocusIn>', clear_default)
    entry_key.bind("<Return>", create_character)
    entry_key.place(
        x=393.0,
        y=520.0,
        width=276.0,
        height=51.0
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        365.0,
        546.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        511.0,
        448.0,
        image=image_image_4
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        531.0,
        448.0,
        image=entry_image_2
    )
    entry_username = Entry(
        bd=0,
        bg="#292929",
        fg="#FFFFFF",  # Set text color to white
        highlightthickness=0
    )
    entry_username.insert(0, "Enter your username")  # Insert default text
    entry_username.bind('<FocusIn>', clear_default)
    entry_key.bind("<Return>", create_character)
    entry_username.place(
        x=393.0,
        y=422.0,
        width=276.0,
        height=51.0
    )

    canvas.create_text(
        397.0,
        440.0,
        anchor="nw",
        text="Enter your username",
        fill="#FFFFFF",
        font=("Inter", 13 * -1)
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        363.0,
        448.0,
        image=image_image_5
    )

    canvas.create_text(
        418.0,
        142.0,
        anchor="nw",
        text="Please Login To Your Account",
        fill="#7B7B7B",
        font=("Inter Light", 13 * -1)
    )

    # Create the "clued" text
    clued_text = canvas.create_text(
        415.0,
        69.0,
        anchor="nw",
        text="Clued",
        fill="#F4F4F4",
        font=("Sedan Regular", 52 * -1)
    )

    # Calculate the width of the "clued" text
    clued_bbox = canvas.bbox(clued_text)
    clued_width = clued_bbox[2] - clued_bbox[0]

    # Create the "AI" text
    canvas.create_text(
        415.0 + clued_width,  # Adjust x-coordinate to center "AI" text relative to "clued" text
        69.0,
        anchor="nw",
        text="AI",
        fill="#D71E1E",
        font=("Sedan Regular", 52 * -1)
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        512.0,
        277.0,
        image=image_image_6
    )

    window.resizable(False, False)
    window.mainloop()
