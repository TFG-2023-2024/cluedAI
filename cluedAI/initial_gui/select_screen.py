from pathlib import Path
from tkinter import BOTH, LEFT, RIGHT, Y, Frame, Label, Scrollbar, Tk, Canvas, Button, PhotoImage
from dotenv import load_dotenv
from db.db_operations import start_day, obtain_by_id, connect_db
from initial_gui.starting_operations import create_window, relative_to_assets

def select():
    window, canvas = create_window("assets/select")
    # Load the environment variables
    load_dotenv()
    _, characters_collection, items_collection, locations_collection, _ = connect_db()
    data = start_day()
    label_font = "Inter Medium"
    left_click = "<Button-1>"

    # Obtain locations by ID where "characters" is not empty
    locations_by_id = [
        obtain_by_id(location_id, locations_collection)
        for location_id in data["locations"]
        if locations_collection.find_one({"_id": location_id, "Characters": {"$exists": True, "$ne": []}})
    ]

    # Lists to store PhotoImage references to prevent garbage collection
    image_refs = []
    button_image_refs = []

    # Load images once to use them multiple times
    background_image = PhotoImage(file=relative_to_assets("item_bg.png"))
    icon_image = PhotoImage(file=relative_to_assets("icon.png"))
    button_image = PhotoImage(file=relative_to_assets("button_1.png"))
    pressed_button_image = PhotoImage(file=relative_to_assets("pressed_button.png"))

    # Store references to prevent garbage collection
    image_refs.append(background_image)
    image_refs.append(icon_image)
    button_image_refs.append(button_image)
    button_image_refs.append(pressed_button_image)

    image_bg = PhotoImage(file=relative_to_assets("bg.png"))
    canvas.create_image(515.0, 390.0, image=image_bg)

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

    # Create the frame to hold the selections and scrollbar
    selection_frame = Frame(window, bg="#202020")
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

    def display_locations():
        '''Display the list of locations.'''
        # Clear the existing content except the scrollbar
        for widget in selection_canvas.winfo_children():
            if widget != scrollbar:
                widget.destroy()

        # Adjust the initial coordinates for each element
        y_offset = 70

        # Create Locations text label
        locations_label = Label(
            selection_canvas,
            text="Locations",
            bg="#202020",
            fg="#D71D1D",
            font=(label_font, 24 * -1)
        )
        locations_label.pack(anchor="nw", padx=106, pady=(0, 50))

        # Iterate over each location and create corresponding elements
        for location in locations_by_id:
            location_id = location["_id"]

            # Create background image first (so it appears behind other elements)
            background_label = Label(selection_canvas, image=background_image, bg="#202020", bd=0)
            background_label.place(x=80, y=y_offset - 15)

            # Create image
            location_label = Label(selection_canvas, image=icon_image, bg="#292929", bd=0)
            location_label.place(x=105, y=y_offset)

            # Create text
            text_label = Label(selection_canvas, text=location['Room'], bg="#292929", fg="#FFFFFF", font=("Inter", 13 * -1))
            text_label.place(x=189, y=y_offset)

            location_button = Canvas(
                selection_canvas,
                width=button_image.width(),
                height=button_image.height(),
                bg="#292929",
                bd=0,
                highlightthickness=0,
                relief="flat"
            )
            location_button.create_image(0, 0, anchor="nw", image=button_image)
            location_button.place(x=916, y=y_offset - 3)

            location_button.bind(left_click, lambda e, loc_id=location_id: display_characters_and_items(loc_id))

            # Update offset for the next iteration
            y_offset += 70  # Adjust this value to set the vertical gap between elements

        # Update the scroll region of the canvas to encompass the frame
        selection_frame.update_idletasks()
        selection_canvas.config(scrollregion=selection_canvas.bbox("all"))

    def display_characters_and_items(location_id):
        '''Display characters and items in the selected location.'''
        # Clear the existing content except the scrollbar
        for widget in selection_canvas.winfo_children():
            if widget != scrollbar:
                widget.destroy()

        # Fetch characters and items in the selected location
        location_data = obtain_by_id(location_id, locations_collection)
        characters = location_data.get("Characters", [])
        items = location_data.get("Items", [])

        # Adjust the initial coordinates for each element
        y_offset = 70

        if characters:
            # Create Characters text label
            characters_label = Label(
                selection_canvas,
                text="Characters",
                bg="#202020",
                fg="#D71D1D",
                font=(label_font, 24 * -1)
            )
            characters_label.pack(anchor="nw", padx=106, pady=(0, 20))

            for character_id in characters:
                character = characters_collection.find_one({"_id": character_id})

                # Create background image first (so it appears behind other elements)
                background_label = Label(selection_canvas, image=background_image, bg="#202020", bd=0)
                background_label.place(x=80, y=y_offset - 15)

                # Create image
                icon_label = Label(selection_canvas, image=icon_image, bg="#292929", bd=0)
                icon_label.place(x=105, y=y_offset)

                # Create text
                text_label = Label(selection_canvas, text=character['Name'], bg="#292929", fg="#FFFFFF", font=("Inter", 13 * -1))
                text_label.place(x=189, y=y_offset)

                character_button = Canvas(
                    selection_canvas,
                    width=button_image.width(),
                    height=button_image.height(),
                    bg="#292929",
                    bd=0,
                    highlightthickness=0,
                    relief="flat"
                )
                character_button.create_image(0, 0, anchor="nw", image=button_image)
                character_button.place(x=916, y=y_offset - 3)

                character_button.bind(left_click, lambda e, char_id=character_id: print(f"Character {char_id} clicked"))

                # Update offset for the next iteration
                y_offset += 70  # Adjust this value to set the vertical gap between elements

        if items:
            # Add space before the items section
            y_offset += 20

            # Create Items text label
            items_label = Label(
                selection_canvas,
                text="Items",
                bg="#202020",
                fg="#D71D1D",
                font=(label_font, 24 * -1)
            )
            items_label.place(x=106, y=y_offset)
            
            # Update y_offset to place items below the items label
            y_offset += 60

            for item_id in items:
                item = items_collection.find_one({"_id": item_id})

                # Create background image first (so it appears behind other elements)
                background_label = Label(selection_canvas, image=background_image, bg="#202020", bd=0)
                background_label.place(x=80, y=y_offset - 15)

                # Create image
                icon_label = Label(selection_canvas, image=icon_image, bg="#292929", bd=0)
                icon_label.place(x=105, y=y_offset)

                # Create text
                text_label = Label(selection_canvas, text=item['Name'], bg="#292929", fg="#FFFFFF", font=("Inter", 13 * -1))
                text_label.place(x=189, y=y_offset)

                item_button = Canvas(
                    selection_canvas,
                    width=button_image.width(),
                    height=button_image.height(),
                    bg="#292929",
                    bd=0,
                    highlightthickness=0,
                    relief="flat"
                )
                item_button.create_image(0, 0, anchor="nw", image=button_image)
                item_button.place(x=916, y=y_offset - 3)

                item_button.bind(left_click, lambda e, itm_id=item_id: print(f"Item {itm_id} clicked"))

                # Update offset for the next iteration
                y_offset += 70  # Adjust this value to set the vertical gap between elements

        # Create back button to return to the locations list
        button_canvas = Canvas(
            canvas,
            width=pressed_button_image.width(),
            height=pressed_button_image.height(),
            bg="#3D3D3D",
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        button_canvas.place(x=304.66650390625 - pressed_button_image.width() // 2, y=40.0 - pressed_button_image.height() // 2)
        button_canvas.create_image(0, 0, anchor="nw", image=pressed_button_image)

        button_canvas.bind(left_click, lambda event: display_locations())

        # Update the scroll region of the canvas to encompass the frame
        selection_canvas.update_idletasks()
        selection_canvas.config(scrollregion=selection_canvas.bbox("all"))

    # Display the initial locations list
    display_locations()

    window.resizable(False, False)
    window.mainloop()

select()
