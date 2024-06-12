from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
from users.user_operations import log_user
from initial_gui.create_screen import create
from initial_gui.starting_operations import create_window, relative_to_assets

def login():
    window, canvas = create_window("assets/login")
    focus = '<FocusIn>'
    username_text = "Enter your username"

    def create_character():
        api = entry_key.get()
        username = entry_username.get()
        
        if not api or not username or api=="Enter your API Key" or username==username_text:
            messagebox.showerror(title='Error', message='Both fields must be completed.', icon="error")
        else:
            log_user(username)
            window.destroy()
            create(username)
        '''
        EDITAR PARA MOSTRAR ERROR CORRECTO YA QUE NO VAMOS A COMPROBAR QUE SEA NUESTRA API KEY
        elif api != "a":  
            messagebox.showerror(title='Error', message='The API key is incorrect.', icon="error")
        '''
        
    image_bg = PhotoImage(
        file=relative_to_assets("bg.png"))
    canvas.create_image(
        515.0,
        403.0,
        image=image_bg
    )

    button_bg = PhotoImage(file=relative_to_assets("login_button.png"))
    login_button = Button(image=button_bg, highlightthickness=0, command=create_character,relief="flat")
    login_button.place(x=334.0, y=634.0, width=355.0, height=53.0)

    image_image_2 = PhotoImage(
        file=relative_to_assets("entry_bg.png"))
    canvas.create_image(
        511.0,
        546.0,
        image=image_image_2
    )

    def clear_default(event):
        event.widget.delete(0, 'end')
        event.widget.unbind(focus)

    entry_bg = PhotoImage(file=relative_to_assets("entry.png"))
    canvas.create_image(531.0, 546.0, image=entry_bg)

    entry_key = Entry(bd=0,bg="#292929",fg="#FFFFFF",font=("Inter", 13 * -1),highlightthickness=0)
    entry_key.insert(0, "Enter your API Key")  # Insert default text
    entry_key.bind(focus, clear_default)
    entry_key.bind("<Return>", create_character)
    entry_key.place(x=393.0,y=521.0,width=276.0,height=51.0)

    image_icon_1 = PhotoImage(
        file=relative_to_assets("icon_1.png"))
    canvas.create_image(
        365.0,
        546.0,
        image=image_icon_1
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("entry_bg.png"))
    canvas.create_image(
        511.0,
        448.0,
        image=image_image_4
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry.png"))
    canvas.create_image(
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
    entry_username.insert(0, username_text)  # Insert default text
    entry_username.bind(focus, clear_default)
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
        text=username_text,
        fill="#FFFFFF",
        font=("Inter", 13 * -1)
    )

    image_icon_2 = PhotoImage(
        file=relative_to_assets("icon_2.png"))
    canvas.create_image(
        363.0,
        448.0,
        image=image_icon_2
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

    image_banner = PhotoImage(
        file=relative_to_assets("banner.png"))
    canvas.create_image(
        512.0,
        277.0,
        image=image_banner
    )

    window.resizable(False, False)
    window.mainloop()
