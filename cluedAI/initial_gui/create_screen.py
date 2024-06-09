from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
from users.user_operations import insert_character
from initial_gui.game_screen import chat

def create(username):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("assets/create")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()

    window.geometry("1024x768")

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

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        512.0,
        277.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        515.0,
        397.56201171875,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        272.0,
        577.0,
        image=image_image_4
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        291.0,
        577.0,
        image=entry_image_1
    )

    def clear_default(event):
            event.widget.delete(0, 'end')
            event.widget.unbind('<FocusIn>')

    entry_gender = Entry(
        bd=0,
        bg="#292929",
        fg="#FFFFFF",
        font=("Inter", 13 * -1),
        highlightthickness=0
    )
    entry_gender.insert(0, "Gender")
    entry_gender.bind('<FocusIn>', clear_default)
    entry_gender.bind("<Return>", submit_character)
    entry_gender.place(
        x=152.0,
        y=551.0,
        width=278.0,
        height=51.0
    )


    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        124.0,
        577.0,
        image=image_image_5
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        272.0,
        446.0,
        image=image_image_6
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        291.0,
        446.0,
        image=entry_image_2
    )

    entry_name = Entry(
        bd=0,
        bg="#292929",
        fg="#FFFFFF",
        font=("Inter", 13 * -1),
        highlightthickness=0
    )

    entry_name.insert(0, "Name")
    entry_name.bind('<FocusIn>', clear_default)
    entry_name.bind("<Return>", submit_character)
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

    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        124.0,
        446.0,
        image=image_image_7
    )

    image_image_8 = PhotoImage(
        file=relative_to_assets("image_8.png"))
    image_8 = canvas.create_image(
        272.0,
        512.0,
        image=image_image_8
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        291.0,
        512.0,
        image=entry_image_3
    )
    entry_age = Entry(
        bd=0,
        bg="#292929",
        fg="#FFFFFF",
        font=("Inter", 13 * -1),
        highlightthickness=0
    )

    entry_age.insert(0, "Age")
    entry_age.bind('<FocusIn>', clear_default)
    entry_age.bind("<Return>", submit_character)
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

    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        124.0,
        512.0,
        image=image_image_9
    )

    image_image_10 = PhotoImage(
        file=relative_to_assets("image_10.png"))
    image_10 = canvas.create_image(
        751.0,
        512.0,
        image=image_image_10
    )

    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(
        769.5,
        512.0,
        image=entry_image_4
    )

    entry_appearance = Entry(
        bd=0,
        bg="#292929",
        fg="#FFFFFF",
        font=("Inter", 13),
        highlightthickness=0
    )

    entry_appearance.insert(0, "Appearance")
    entry_appearance.bind('<FocusIn>', clear_default)
    entry_appearance.bind("<Return>", submit_character)
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

    image_image_11 = PhotoImage(
        file=relative_to_assets("image_11.png"))
    image_11 = canvas.create_image(
        601.0,
        513.0,
        image=image_image_11
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        highlightthickness=0,
        command=submit_character,
        relief="flat"
    )
    button_1.place(
        x=338.0,
        y=642.0,
        width=355.0,
        height=53.0
    )
    window.resizable(False, False)
    window.mainloop()
