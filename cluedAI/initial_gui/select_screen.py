from pathlib import Path

from tkinter import BOTH, LEFT, RIGHT, Frame, Scrollbar, Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/aya/Documents/tfg/cluedAI/cluedAI/initial_gui/assets/select_v0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1024x768")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
        window,
        bg="#202020",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
canvas.place(x=0, y=0)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    515.0,
    403.0,
    image=image_image_1
)

image_image_0 = PhotoImage(file=relative_to_assets("image_0.png"))
image_0 = canvas.create_image(510, 40, image=image_image_0)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    304.66650390625,
    40.0,
    image=image_image_2
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

image_image_11 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_11 = canvas.create_image(
    516,
    196,
    image=image_image_11
)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))

def select_op():
    pass

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))

button_canvas = Canvas(
        canvas,
        width=button_image_1.width(),
        height=button_image_1.height(),
        bg="#292929",
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
button_canvas.place(x=914.0, y=181.0)
button_canvas.create_image(0, 0, anchor="nw", image=button_image_1)
button_canvas.bind("<Button-1>", select_op)

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

image_5 = canvas.create_image(
    105.0,
    261.7391357421875,
    image=image_image_4
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

image_6 = canvas.create_image(
    105.0,
    381.7391357421875,
    image=image_image_4
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

image_7 = canvas.create_image(
    105.0,
    512.7391357421875,
    image=image_image_4
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

image_8 = canvas.create_image(
    105.0,
    447.478271484375,
    image=image_image_4
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

image_9 = canvas.create_image(
    101.0,
    619.7391357421875,
    image=image_image_4
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

image_10 = canvas.create_image(
    101.0,
    685.478271484375,
    image=image_image_4
)

canvas.create_text(
    185.0,
    676.478271484375,
    anchor="nw",
    text="Who Is Richest Person?",
    fill="#FFFFFF",
    font=("Inter", 13 * -1)
)

'''
# Create the frame to hold the messages list and scrollbar
selection_frame = Frame(window)
selection_frame.place(x=12, y=100, width=1000, height=520)

scrollbar = Scrollbar(selection_frame, orient="vertical")
scrollbar.pack(side=RIGHT, fill=Y)

selection_canvas = Canvas(selection_frame, bg="#202020", bd=0, highlightthickness=0, yscrollcommand=scrollbar.set)
selection_canvas.pack(side=LEFT, fill=BOTH, expand=True)

selection = []

scrollbar.config(command=selection_canvas.yview)

def on_mouse_wheel(event):
    selection_canvas.yview_scroll(-1 * event.delta, 'units')

# Bind mouse wheel events for Windows and MacOS
window.bind_all("<MouseWheel>", on_mouse_wheel)
'''

window.resizable(False, False)
window.mainloop()
