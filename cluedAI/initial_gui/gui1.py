
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/aya/Documents/tfg/cluedAI/cluedAI/initial_gui/assets/frame1")


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
    260.0,
    0.0,
    763.00048828125,
    85.00000000000023,
    fill="#3C3C3C",
    outline="")

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    304.66650390625,
    40.0,
    image=image_image_2
)

canvas.create_text(
    454.0,
    22.0,
    anchor="nw",
    text="CluedAI",
    fill="#F4F4F4",
    font=("Inter", 30 * -1)
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    712.0,
    40.0,
    image=image_image_3
)

canvas.create_text(
    106.0,
    126.0,
    anchor="nw",
    text="Characters",
    fill="#D71D1D",
    font=("Inter Medium", 24 * -1)
)

canvas.create_text(
    105.58544921875,
    556.4456787109375,
    anchor="nw",
    text="Objects\n",
    fill="#D71D1D",
    font=("Inter Medium", 24 * -1)
)

canvas.create_text(
    106.0,
    317.0,
    anchor="nw",
    text="Locations\n",
    fill="#D71D1D",
    font=("Inter Medium", 24 * -1)
)

canvas.create_rectangle(
    71.0,
    169.2608642578125,
    961.0,
    222.25542831420898,
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
    x=906.0,
    y=175.0,
    width=42.0,
    height=41.999977111816406
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    105.0,
    196.0,
    image=image_image_4
)

canvas.create_text(
    189.0,
    187.0,
    anchor="nw",
    text="Who Is Richest Person?",
    fill="#FFFFFF",
    font=("Inter", 13 * -1)
)

canvas.create_rectangle(
    71.0,
    235.0,
    961.0,
    287.9945640563965,
    fill="#292929",
    outline="")

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=906.0,
    y=240.7391357421875,
    width=42.0,
    height=41.999977111816406
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    105.0,
    261.7391357421875,
    image=image_image_5
)

canvas.create_text(
    189.0,
    252.7391357421875,
    anchor="nw",
    text="Who Is Richest Person?",
    fill="#FFFFFF",
    font=("Inter", 13 * -1)
)

canvas.create_rectangle(
    71.0,
    355.0,
    961.0,
    407.9945640563965,
    fill="#292929",
    outline="")

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=906.0,
    y=360.7391357421875,
    width=42.0,
    height=41.999977111816406
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    105.0,
    381.7391357421875,
    image=image_image_6
)

canvas.create_text(
    189.0,
    372.7391357421875,
    anchor="nw",
    text="Who Is Richest Person?",
    fill="#FFFFFF",
    font=("Inter", 13 * -1)
)

canvas.create_rectangle(
    71.0,
    486.0,
    961.0,
    538.9945640563965,
    fill="#292929",
    outline="")

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=906.0,
    y=491.7391357421875,
    width=42.0,
    height=41.999977111816406
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    105.0,
    512.7391357421875,
    image=image_image_7
)

canvas.create_text(
    189.0,
    503.7391357421875,
    anchor="nw",
    text="Who Is Richest Person?",
    fill="#FFFFFF",
    font=("Inter", 13 * -1)
)

canvas.create_rectangle(
    71.0,
    420.7391357421875,
    961.0,
    473.733699798584,
    fill="#292929",
    outline="")

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=906.0,
    y=426.478271484375,
    width=42.0,
    height=41.999977111816406
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    105.0,
    447.478271484375,
    image=image_image_8
)

canvas.create_text(
    189.0,
    438.478271484375,
    anchor="nw",
    text="Who Is Richest Person?",
    fill="#FFFFFF",
    font=("Inter", 13 * -1)
)

canvas.create_rectangle(
    67.0,
    593.0,
    957.0,
    645.9945640563965,
    fill="#292929",
    outline="")

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat"
)
button_6.place(
    x=902.0,
    y=598.7391357421875,
    width=42.0,
    height=41.999977111816406
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    101.0,
    619.7391357421875,
    image=image_image_9
)

canvas.create_text(
    185.0,
    610.7391357421875,
    anchor="nw",
    text="Who Is Richest Person?",
    fill="#FFFFFF",
    font=("Inter", 13 * -1)
)

canvas.create_rectangle(
    67.0,
    658.7391357421875,
    957.0,
    711.733699798584,
    fill="#292929",
    outline="")

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_7 clicked"),
    relief="flat"
)
button_7.place(
    x=902.0,
    y=664.478271484375,
    width=42.0,
    height=41.999977111816406
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    101.0,
    685.478271484375,
    image=image_image_10
)

canvas.create_text(
    185.0,
    676.478271484375,
    anchor="nw",
    text="Who Is Richest Person?",
    fill="#FFFFFF",
    font=("Inter", 13 * -1)
)
window.resizable(False, False)
window.mainloop()
