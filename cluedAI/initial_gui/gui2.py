
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame2")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1024x768")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
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

canvas.create_rectangle(
    0.0,
    631.0,
    1024.0,
    768.0,
    fill="#292929",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=916.0,
    y=663.0,
    width=73.34676361083984,
    height=73.34676361083984
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    461.0,
    698.5,
    image=entry_image_1
)
entry_1 = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=56.0,
    y=673.0,
    width=810.0,
    height=49.0
)

canvas.create_rectangle(
    260.0,
    0.0,
    763.00048828125,
    85.00000000000023,
    fill="#3C3C3C",
    outline="")

canvas.create_text(
    454.0,
    22.0,
    anchor="nw",
    text="CluedAI",
    fill="#F4F4F4",
    font=("Inter", 30 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    304.66650390625,
    40.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    712.0,
    40.0,
    image=image_image_3
)

canvas.create_rectangle(
    36.0,
    134.0,
    461.0,
    285.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    840.0,
    328.0,
    992.0,
    392.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    36.0,
    447.0,
    461.0,
    583.0,
    fill="#000000",
    outline="")
window.resizable(False, False)
window.mainloop()
