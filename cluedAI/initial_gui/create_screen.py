from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
from users.user_operations import insert_character
from initial_gui.game_screen import chat
from initial_gui.starting_operations import create_window, relative_to_assets

def create(username):
    window, canvas = create_window("assets/create")
    focus = '<FocusIn>'
    back = "<Return>"

    def submit_character():
        data = {
            "Name": entry_name.get(),
            "Age": entry_age.get(),
            "Gender": entry_gender.get(),
            "Appearance": entry_appearance.get()
        }

        if not data["Name"] or not data["Age"] or not data["Gender"] or not data["Appearance"]:
            messagebox.showerror(title='Error', message='All fields must be completed.')
        else:
            insert_character(username, data)
            window.destroy()
            chat()

    image_bg = PhotoImage(
        file=relative_to_assets("bg.png"))
    canvas.create_image(
        515.0,
        403.0,
        image=image_bg
    )

    canvas.create_text(
        427.0,
        142.0,
        anchor="nw",
        text="Create your own character!",
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

    image_divider = PhotoImage(
        file=relative_to_assets("divider.png"))
    canvas.create_image(
        515.0,
        397.56201171875,
        image=image_divider
    )

    entry_bg_1 = PhotoImage(
        file=relative_to_assets("entry_bg_1.png"))
    canvas.create_image(
        272.0,
        577.0,
        image=entry_bg_1
    )

    entry_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    canvas.create_image(
        291.0,
        577.0,
        image=entry_1
    )

    def clear_default(event):
            event.widget.delete(0, 'end')
            event.widget.unbind(focus)

    entry_gender = Entry(
        bd=0,
        bg="#292929",
        fg="#FFFFFF",
        font=("Inter", 13 * -1),
        highlightthickness=0
    )
    entry_gender.insert(0, "Gender")
    entry_gender.bind(focus, clear_default)
    entry_gender.bind(back, submit_character)
    entry_gender.place(
        x=152.0,
        y=551.0,
        width=278.0,
        height=51.0
    )


    icon = PhotoImage(
        file=relative_to_assets("icon.png"))
    canvas.create_image(
        124.0,
        577.0,
        image=icon
    )

    canvas.create_image(
        272.0,
        446.0,
        image=entry_bg_1
    )

    canvas.create_image(
        291.0,
        446.0,
        image=entry_1
    )

    entry_name = Entry(
        bd=0,
        bg="#292929",
        fg="#FFFFFF",
        font=("Inter", 13 * -1),
        highlightthickness=0
    )

    entry_name.insert(0, "Name")
    entry_name.bind(focus, clear_default)
    entry_name.bind(back, submit_character)
    entry_name.place(
        x=152.0,
        y=420.0,
        width=278.0,
        height=51.0
    )

    canvas.create_text(
        158.0,
        438.0,
        anchor="nw",
        text="Name",
        fill="#FFFFFF",
        font=("Inter", 13 * -1)
    )

    canvas.create_image(
        124.0,
        446.0,
        image=icon
    )

    canvas.create_image(
        272.0,
        512.0,
        image=entry_bg_1
    )

    canvas.create_image(
        291.0,
        512.0,
        image=entry_1
    )

    entry_age = Entry(
        bd=0,
        bg="#292929",
        fg="#FFFFFF",
        font=("Inter", 13 * -1),
        highlightthickness=0
    )

    entry_age.insert(0, "Age")
    entry_age.bind(focus, clear_default)
    entry_age.bind(back, submit_character)
    entry_age.place(
        x=152.0,
        y=486.0,
        width=278.0,
        height=51.0
    )

    canvas.create_text(
        158.0,
        504.0,
        anchor="nw",
        text="Age",
        fill="#FFFFFF",
        font=("Inter", 13 * -1)
    )

    canvas.create_image(
        124.0,
        512.0,
        image=icon
    )

    entry_bg_2 = PhotoImage(
        file=relative_to_assets("entry_bg_2.png"))
    canvas.create_image(
        751.0,
        512.0,
        image=entry_bg_2
    )

    entry_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    
    canvas.create_image(
        769.5,
        512.0,
        image=entry_2
    )

    entry_appearance = Entry(
        bd=0,
        bg="#292929",
        fg="#FFFFFF",
        font=("Inter", 13),
        highlightthickness=0
    )

    entry_appearance.insert(0, "Appearance")
    entry_appearance.bind(focus, clear_default)
    entry_appearance.bind(back, submit_character)
    entry_appearance.place(
        x=629.0,
        y=421.0,
        width=281.0,
        height=181.0
    )

    canvas.create_text(
        637.72509765625,
        505.2651062011719,
        anchor="nw",
        text="Appearance",
        fill="#FFFFFF",
        font=("Inter", 13 * -1)
    )

    canvas.create_image(
        601.0,
        513.0,
        image=icon
    )

    submit_button_image = PhotoImage(
        file=relative_to_assets("submit_button.png"))
    
    submit_button = Button(
        image=submit_button_image,
        highlightthickness=0,
        command=submit_character,
        relief="flat"
    )

    submit_button.place(
        x=338.0,
        y=642.0,
        width=355.0,
        height=53.0
    )

    window.resizable(False, False)
    window.mainloop()
