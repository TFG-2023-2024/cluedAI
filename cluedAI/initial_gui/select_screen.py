import os
from pathlib import Path
from tkinter import BOTH, LEFT, RIGHT, Y, Frame, Label, Scrollbar, Tk, Canvas, Button, PhotoImage
from dotenv import load_dotenv
from db.db_operations import start_day, obtain_by_id, connect_db

def select():
    # Load the environment variables
    load_dotenv()
    _, characters_collection, items_collection, locations_collection, _ = connect_db()
    data = start_day()

    # Obtain locations by ID where "characters" is not empty
    locations_by_id = [
        obtain_by_id(location_id, locations_collection)
        for location_id in data["locations"]
        if locations_collection.find_one({"_id": location_id, "Characters": {"$exists": True, "$ne": []}})
    ]

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

    # Lists to store PhotoImage references to prevent garbage collection
    image_refs = []
    button_image_refs = []

    # Load images once to use them multiple times
    background_image = PhotoImage(file=relative_to_assets("item_bg.png"))
    icon_image = PhotoImage(file=relative_to_assets("icon.png"))
    button_image = PhotoImage(file=relative_to_assets("button_1.png"))

    # Store references to prevent garbage collection
    image_refs.append(background_image)
    image_refs.append(icon_image)
    button_image_refs.append(button_image)

    image_bg = PhotoImage(file=relative_to_assets("bg.png"))
    canvas.create_image(515.0, 403.0, image=image_bg)

    image_banner = PhotoImage(file=relative_to_assets("banner.png"))
    canvas.create_image(510, 40, image=image_banner)

    image_pressed_button = PhotoImage(file=relative_to_assets("pressed_button.png"))
    canvas.create_image(304.66650390625, 40.0, image=image_pressed_button)

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

    # Create Locations text label
    locations_label = Label(
        selection_frame,
        text="Locations",
        bg="#202020",
        fg="#D71D1D",
        font=("Inter Medium", 24 * -1)
    )
    locations_label.place(x=106.0, y=50.0, anchor="nw")

    def display_characters_and_items(location_id, canvas):
        """Display characters and items in the selected location."""
        # Clear the existing content
        for widget in selection_frame.winfo_children():
            widget.destroy()

        # Fetch characters and items in the selected location
        location_data = obtain_by_id(location_id, locations_collection)
        characters = location_data.get("Characters", [])
        items = location_data.get("Items", [])

        # Adjust the initial coordinates for each element
        y_offset = 110

        if characters:
            # Create Characters text label
            characters_label = Label(
                selection_frame,
                text="Characters",
                bg="#202020",
                fg="#D71D1D",
                font=("Inter Medium", 24 * -1)
            )
            characters_label.place(x=106.0, y=50.0, anchor="nw")

            for character_id in characters:
                character = characters_collection.find_one({"_id": character_id})

                # Create background image first (so it appears behind other elements)
                background_label = Label(selection_frame, image=background_image, bg="#202020", bd=0)
                background_label.place(x=80, y=y_offset - 15)

                # Create image
                icon_label = Label(selection_frame, image=icon_image, bg="#292929", bd=0)
                icon_label.place(x=105, y=y_offset)

                # Create text
                text_label = Label(selection_frame, text=character['Name'], bg="#292929", fg="#FFFFFF", font=("Inter", 13 * -1))
                text_label.place(x=189, y=y_offset)

                character_button = Canvas(
                    selection_frame,
                    width=button_image.width(),
                    height=button_image.height(),
                    bg="#292929",
                    bd=0,
                    highlightthickness=0,
                    relief="flat"
                )
                character_button.create_image(0, 0, anchor="nw", image=button_image)
                character_button.place(x=916, y=y_offset - 3)

                character_button.bind("<Button-1>", lambda e, char_id=character_id: print(f"Character {char_id} clicked"))

                # Update offset for the next iteration
                y_offset += 70  # Adjust this value to set the vertical gap between elements

        if items:
            # Create Items text label
            items_label = Label(
                selection_frame,
                text="Items",
                bg="#202020",
                fg="#D71D1D",
                font=("Inter Medium", 24 * -1)
            )
            items_label.place(x=106.0, y=y_offset + 20, anchor="nw")

            y_offset += 70  # Adjust this value to set the vertical gap between elements

            for item_id in items:
                item = items_collection.find_one({"_id": item_id})

                # Create background image first (so it appears behind other elements)
                background_label = Label(selection_frame, image=background_image, bg="#202020", bd=0)
                background_label.place(x=80, y=y_offset - 15)

                # Create image
                icon_label = Label(selection_frame, image=icon_image, bg="#292929", bd=0)
                icon_label.place(x=105, y=y_offset)

                # Create text
                text_label = Label(selection_frame, text=item['Name'], bg="#292929", fg="#FFFFFF", font=("Inter", 13 * -1))
                text_label.place(x=189, y=y_offset)

                item_button = Canvas(
                    selection_frame,
                    width=button_image.width(),
                    height=button_image.height(),
                    bg="#292929",
                    bd=0,
                    highlightthickness=0,
                    relief="flat"
                )
                item_button.create_image(0, 0, anchor="nw", image=button_image)
                item_button.place(x=916, y=y_offset - 3)

                item_button.bind("<Button-1>", lambda e, itm_id=item_id: print(f"Item {itm_id} clicked"))

                # Update offset for the next iteration
                y_offset += 70  # Adjust this value to set the vertical gap between elements

        # Update the scroll region of the canvas to encompass the frame
        selection_frame.update_idletasks()
        selection_canvas.config(scrollregion=selection_canvas.bbox("all"))

    # Adjust the initial coordinates for each element
    y_offset = 110
    
    # Iterate over each location and create corresponding elements
    for location in locations_by_id:
        location_id = location["_id"]

        # Create background image first (so it appears behind other elements)
        background_label = Label(selection_frame, image=background_image, bg="#202020", bd=0)
        background_label.place(x=80, y=y_offset - 15)

        # Create image
        location_label = Label(selection_frame, image=icon_image, bg="#292929", bd=0)
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

        location_button.bind("<Button-1>", lambda e, loc_id=location_id: display_characters_and_items(loc_id, selection_canvas))

        # Update offset for the next iteration
        y_offset += 70  # Adjust this value to set the vertical gap between elements

    # Update the scroll region of the canvas to encompass the frame
    selection_frame.update_idletasks()
    selection_canvas.config(scrollregion=selection_canvas.bbox("all"))

    window.resizable(False, False)
    window.mainloop()

select()
