import os
from pathlib import Path
from tkinter import BOTH, LEFT, RIGHT, VERTICAL, Y, Frame, Label, Scrollbar, Tk, Canvas, Entry, Text, Button, PhotoImage
from dotenv import load_dotenv
from db.db_operations import start_day, obtain_by_id, connect_db

def select():
    # Load the environment variables
    load_dotenv()
    _, characters_collection, items_collection, locations_collection, _ = connect_db()
    data = start_day()
    # Obtain locations by ID
    locations_by_id = [obtain_by_id(location_id, locations_collection) for location_id in data["locations"]]
    day = int(os.getenv('DAY'))

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"assets/select_v0")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.geometry("1024x768")
    window.configure(bg="#FFFFFF")

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

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(515.0, 403.0, image=image_image_1)

    image_image_0 = PhotoImage(file=relative_to_assets("image_0.png"))
    image_0 = canvas.create_image(510, 40, image=image_image_0)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(304.66650390625, 40.0, image=image_image_2)

    # Create the "Clued" text
    clued_text = canvas.create_text(
        454.0,
        22.0,
        anchor="nw",
        text="Clued",
        fill="#F4F4F4",
        font=("Inter", 30 * -1)
    )

    # Calculate the width of the "Clued" text
    clued_bbox = canvas.bbox(clued_text)
    clued_width = clued_bbox[2] - clued_bbox[0]

    # Create the "AI" text
    canvas.create_text(
        454.0 + clued_width,  # Adjust x-coordinate to center "AI" text relative to "Clued" text
        22.0,
        anchor="nw",
        text="AI",
        fill="#D71E1E",
        font=("Inter", 30 * -1)
    )

    ###################################################################################################
    # Create the frame to hold the selections and scrollbar
    selection_frame = Frame(window)
    selection_frame.place(x=0, y=100, width=1024, height=658)

    scrollbar = Scrollbar(selection_frame, orient="vertical")
    scrollbar.pack(side=RIGHT, fill=Y)

    selection_canvas = Canvas(selection_frame, bg="#202020", bd=0, highlightthickness=0, yscrollcommand=scrollbar.set)
    selection_canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar.config(command=selection_canvas.yview)

    def on_mouse_wheel(event):
        selection_canvas.yview_scroll(-1 * event.delta, 'units')

    # Bind mouse wheel events for Windows and MacOS
    window.bind_all("<MouseWheel>", on_mouse_wheel)

    if day >= 1:
        # Create Characters text label
        characters_label = Label(
            selection_frame,
            text="Characters",
            bg="#202020",
            fg="#D71D1D",
            font=("Inter Medium", 24 * -1)
        )
        characters_label.place(x=106.0, y=126.0, anchor="nw")

        # Create Objects text label
        objects_label = Label(
            selection_frame,
            text="Objects",
            bg="#202020",
            fg="#D71D1D",
            font=("Inter Medium", 24 * -1)
        )
        objects_label.place(x=106.0, y=556.4456787109375, anchor="nw")

        # Create Locations text label
        locations_label = Label(
            selection_frame,
            text="Locations",
            bg="#202020",
            fg="#D71D1D",
            font=("Inter Medium", 24 * -1)
        )
        locations_label.place(x=106.0, y=317.0, anchor="nw")
    else:
        # Create Locations text label
        locations_label = Label(
            selection_frame,
            text="Locations",
            bg="#202020",
            fg="#D71D1D",
            font=("Inter Medium", 24 * -1)
        )
        locations_label.place(x=106.0, y=50.0, anchor="nw")
        # Adjust the initial coordinates for each element
        x_offset = 105
        y_offset = 110

    def select_op():
        pass

    # Lists to store PhotoImage references to prevent garbage collection
    image_refs = []
    button_image_refs = []

    # Load images once to use them multiple times
    background_image = PhotoImage(file=relative_to_assets("image_5.png"))
    location_image = PhotoImage(file=relative_to_assets("image_4.png"))
    button_image = PhotoImage(file=relative_to_assets("button_1.png"))

    # Store references to prevent garbage collection
    image_refs.append(background_image)
    image_refs.append(location_image)
    button_image_refs.append(button_image)

    # Iterate over each location and create corresponding elements
    for location in locations_by_id:
        
        # Create background image first (so it appears behind other elements)
        background_label = Label(selection_frame, image=background_image, bg="#202020", bd=0)
        background_label.place(x=80, y=y_offset - 15)

        # Create image
        location_label = Label(selection_frame, image=location_image, bg="#292929", bd=0)
        location_label.place(x=105, y=y_offset)

        # Create text
        text_label = Label(selection_frame, text=location['Room'], bg="#292929", fg="#FFFFFF", font=("Inter", 13 * -1))
        text_label.place(x=189, y=y_offset)

        location_button = Canvas(
            selection_frame,
            width=button_image.width(),
            height=button_image.height(),
            bg="#292929",
            bd=0,
            highlightthickness=0,
            relief="flat"
        )
        location_button.create_image(0, 0, anchor="nw", image=button_image)
        location_button.place(x=916, y=y_offset - 3)

        location_button.bind("<Button-1>", select_op)

        
        # Update offset for the next iteration
        y_offset += 70  # Adjust this value to set the vertical gap between elements

    # Update the scroll region of the canvas to encompass the frame
    selection_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    ###################################################################################################


    """ canvas.create_rectangle(
        71.0,
        235.0,
        961.0,
        287.9945640563965,
        fill="#292929",
        outline=""
    )

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
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

    image_5 = canvas.create_image(105.0, 261.7391357421875, image=image_image_4)

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
        outline=""
    )

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
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

    image_6 = canvas.create_image(105.0, 381.7391357421875, image=image_image_4)

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
        outline=""
    )

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
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

    image_7 = canvas.create_image(105.0, 512.7391357421875, image=image_image_4)

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
        outline=""
    )

    button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
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

    image_8 = canvas.create_image(105.0, 447.478271484375, image=image_image_4)

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
        outline=""
    )

    button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
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

    image_9 = canvas.create_image(101.0, 619.7391357421875, image=image_image_4)

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
        outline=""
    )

    button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
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

    image_10 = canvas.create_image(101.0, 685.478271484375, image=image_image_4)

    canvas.create_text(
        185.0,
        676.478271484375,
        anchor="nw",
        text="Who Is Richest Person?",
        fill="#FFFFFF",
        font=("Inter", 13 * -1)
    ) """

    window.resizable(False, False)
    window.mainloop()
