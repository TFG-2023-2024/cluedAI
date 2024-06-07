from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
from initial_gui.login_screen import login

def start():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/aya/Documents/tfg/cluedAI/cluedAI/initial_gui/assets/start")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def open_login():
        window.destroy()
        login()

    window = Tk()

    window.geometry("1024x768")

    canvas = Canvas(
        window,
        bg = "#000000",
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
        512.0,
        349.0,
        image=image_image_1
    )

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        highlightthickness=1,
        command=open_login,
        relief="flat"
    )
    button_1.place(
        x=334.0,
        y=667.0,
        width=355.0,
        height=53.0
    )

    # Create the "clued" text
    clued_text = canvas.create_text(
        288.5,  # Center horizontally
        325.0,
        anchor="nw",
        text="clued",
        fill="#FFFFFF",
        font=("Inter SemiBold", 140 * -1)
    )

    # Calculate the width of the "clued" text
    clued_bbox = canvas.bbox(clued_text)
    clued_width = clued_bbox[2] - clued_bbox[0]

    # Create the "AI" text
    canvas.create_text(
        288.5 + clued_width,  # Adjust x-coordinate to center "AI" text relative to "clued" text
        325.0,
        anchor="nw",
        text="AI",
        fill="#D71E1E",
        font=("Inter Bold", 140 * -1)
    )

    canvas.create_text(
        267.0,
        483.0,
        anchor="nw",
        text="Embark on an enthralling journey through CluedAI, a murder" + 
        "\nmystery interactive visual novel powered by generative AI. Delve" + 
        "\ninto a meticulously crafted narrative where every decision shapes" + 
        "\nthe investigation's outcome. Uncover clues, interrogate suspects," +
        "\nand navigate through twists and turns as you strive to solve the crime.",
        fill="#FFFFFF",
        font=("Inter", 18 * -1)
    )

    window.resizable(False, False)
    window.mainloop()
