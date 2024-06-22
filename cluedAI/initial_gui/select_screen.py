from tkinter import BOTH, LEFT, RIGHT, Y, Frame, Label, Scrollbar, Canvas, PhotoImage, Tk
from dotenv import load_dotenv
from db.db_operations import obtain_by_id, connect_db
from initial_gui.starting_operations import create_window, relative_to_assets

class SelectScreen:
    def __init__(self, root, switch_to_chat, day, data):
        """
        Initialize the SelectScreen object with necessary attributes and UI setup.

        Args:
        - root (Tk): The root Tkinter window.
        - switch_to_chat (function): Function to switch to the chat interface.
        - day (int): The current day of the game.
        - data (dict): Data containing game-specific information.
        """
        self.root = root
        self.switch_to_chat = switch_to_chat
        self.day = day
        self.data = data
        self.label_font = "Inter Medium"
        self.left_click = "<Button-1>"
        self.window, self.canvas = create_window("assets/select", existing_root=root)
        load_dotenv()
        global characters_collection, items_collection, locations_collection
        _, characters_collection, items_collection, locations_collection, _, _ = connect_db()
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface elements for the SelectScreen.

        This includes loading images, creating canvas elements, and preparing UI components.
        """
        self.locations_by_id = [
            obtain_by_id(location_id, locations_collection)
            for location_id in self.data.get("locations", [])
            if locations_collection.find_one({"_id": location_id, "Characters": {"$exists": True, "$ne": []}})
        ]

        self.calendar_image = PhotoImage(file=relative_to_assets("calendar.png"))
        self.background_image = PhotoImage(file=relative_to_assets("item_bg.png"))
        self.icon_image = PhotoImage(file=relative_to_assets("icon.png"))
        self.button_image = PhotoImage(file=relative_to_assets("button_1.png"))
        self.pressed_button_image = PhotoImage(file=relative_to_assets("pressed_button.png"))
        self.image_bg = PhotoImage(file=relative_to_assets("bg.png"))
        self.image_banner = PhotoImage(file=relative_to_assets("banner.png"))

        # Store references to prevent garbage collection
        self.image_refs = [
            self.calendar_image, self.background_image, self.icon_image, self.image_bg, self.image_banner
        ]
        self.button_image_refs = [
            self.button_image, self.pressed_button_image
        ]

        self.create_canvas_elements()

    def create_canvas_elements(self):
        """
        Create canvas elements for the main UI of the ChatScreen.

        This method initializes various graphical elements on the canvas, including text, images, and buttons.
        """
        self.canvas.create_image(515.0, 390.0, image=self.image_bg)
        self.canvas.create_image(510, 40, image=self.image_banner)
        self.canvas.create_image(304.66650390625, 40.0, image=self.pressed_button_image)

        clued_text = self.canvas.create_text(
            454.0,
            22.0,
            anchor="nw",
            text="Clued",
            fill="#F4F4F4",
            font=("Inter", 30 * -1)
        )

        clued_bbox = self.canvas.bbox(clued_text)
        clued_width = clued_bbox[2] - clued_bbox[0]

        self.canvas.create_text(
            454.0 + clued_width,
            22.0,
            anchor="nw",
            text="AI",
            fill="#D71E1E",
            font=("Inter", 30 * -1)
        )

        self.canvas.create_image(38, 60.0 - self.calendar_image.height() // 2, image=self.calendar_image)
        self.day_label = self.canvas.create_text(
            31.0,
            28.0,
            anchor="nw",
            text=str(self.day),
            fill="#D71E1E",
            font=("Inter", 24)
        )

        self.create_selection_frame()

    def create_selection_frame(self):
        """
        Create the selection frame for displaying characters or locations.

        This method creates a scrollable canvas within a frame to display selectable options.
        """
        selection_frame = Frame(self.window, bg="#202020")
        selection_frame.place(x=0, y=100, width=1024, height=658)

        scrollbar = Scrollbar(selection_frame, orient="vertical")
        scrollbar.pack(side=RIGHT, fill=Y)

        selection_canvas = Canvas(selection_frame, bg="#202020", bd=0, highlightthickness=0, yscrollcommand=scrollbar.set)
        selection_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar.config(command=selection_canvas.yview)

        def on_mouse_wheel(event):
            selection_canvas.yview_scroll(-1 * (event.delta // 120), 'units')

        self.window.bind_all("<MouseWheel>", on_mouse_wheel)

        self.selection_canvas = selection_canvas
        if self.day == 5:
            self.display_murderer_selection()
        else:
            self.display_locations()

    def display_murderer_selection(self):
        """
        Display the selection interface for identifying the murderer.

        This method populates the selection canvas with character options excluding the victim(s).
        """
        if self.day != 5:
            return

        for widget in self.selection_canvas.winfo_children():
            widget.destroy()

        y_offset = 65

        characters_label = Label(
            self.selection_canvas,
            text="Who is the murderer?",
            bg="#202020",
            fg="#D71D1D",
            font=(self.label_font, 24 * -1)
        )
        characters_label.pack(anchor="nw", padx=106, pady=(0, 20))

        # Fetch all characters and filter out victims
        all_characters = list(characters_collection.find())
        non_victim_characters = [
            character for character in all_characters
            if character['Archetype'] != "Victim"
        ]

        for character in non_victim_characters:
            character_id = character["_id"]

            background_label = Label(self.selection_canvas, image=self.background_image, bg="#202020", bd=0)
            background_label.place(x=80, y=y_offset - 15)

            icon_label = Label(self.selection_canvas, image=self.icon_image, bg="#292929", bd=0)
            icon_label.place(x=105, y=y_offset)

            text_label = Label(self.selection_canvas, text=f"{character['Name']} {character['Surname']}", bg="#292929", fg="#FFFFFF", font=("Inter", 13 * -1))
            text_label.place(x=189, y=y_offset)

            character_button = Canvas(
                self.selection_canvas,
                width=self.button_image.width(),
                height=self.button_image.height(),
                bg="#292929",
                bd=0,
                highlightthickness=0,
                relief="flat"
            )
            character_button.create_image(0, 0, anchor="nw", image=self.button_image)
            character_button.place(x=916, y=y_offset - 3)

            character_button.bind(self.left_click, lambda e, char_id=character_id: self.select_character(char_id))

            y_offset += 65  # Increment y_offset for the next character entry

        self.selection_canvas.update_idletasks()
        self.selection_canvas.config(scrollregion=self.selection_canvas.bbox("all"))

    def display_locations(self):
        """
        Display the selection interface for choosing locations.

        This method populates the selection canvas with available locations based on game data.
        """
        for widget in self.selection_canvas.winfo_children():
            widget.destroy()

        y_offset = 70

        locations_label = Label(
            self.selection_canvas,
            text="Locations",
            bg="#202020",
            fg="#D71D1D",
            font=(self.label_font, 24 * -1)
        )
        locations_label.pack(anchor="nw", padx=106, pady=(0, 50))

        for location in self.locations_by_id:
            location_id = location["_id"]

            # Check if the location has characters or items
            if not location['Characters'] and not location['Items']:
                continue

            background_label = Label(self.selection_canvas, image=self.background_image, bg="#202020", bd=0)
            background_label.place(x=80, y=y_offset - 15)

            icon_label = Label(self.selection_canvas, image=self.icon_image, bg="#292929", bd=0)
            icon_label.place(x=105, y=y_offset)

            text_label = Label(self.selection_canvas, text=location['Room'], bg="#292929", fg="#FFFFFF", font=("Inter", 13 * -1))
            text_label.place(x=189, y=y_offset)

            location_button = Canvas(
                self.selection_canvas,
                width=self.button_image.width(),
                height=self.button_image.height(),
                bg="#292929",
                bd=0,
                highlightthickness=0,
                relief="flat"
            )
            location_button.create_image(0, 0, anchor="nw", image=self.button_image)
            location_button.place(x=916, y=y_offset - 3)

            location_button.bind(self.left_click, lambda e, loc_id=location_id: self.display_characters_and_items(loc_id))

            y_offset += 70

        self.selection_canvas.update_idletasks()
        self.selection_canvas.config(scrollregion=self.selection_canvas.bbox("all"))

    def display_characters_and_items(self, location_id):
        """
        Display characters and items for the selected location on the canvas.

        This method populates the selection canvas with characters and items based on
        the location ID provided. It creates UI elements for each character and item,
        allowing users to select them.

        Args:
        - location_id (str): The ID of the location to display characters and items for.
        """
        for widget in self.selection_canvas.winfo_children():
            widget.destroy()

        location_data = obtain_by_id(location_id, locations_collection)
        characters = location_data.get("Characters", [])
        items = location_data.get("Items", [])

        y_offset = 70

        non_victim_characters = [character_id for character_id in characters if characters_collection.find_one({"_id": character_id})['Archetype'] != "Victim"]

        if non_victim_characters:
            characters_label = Label(
                self.selection_canvas,
                text="Characters",
                bg="#202020",
                fg="#D71D1D",
                font=(self.label_font, 24 * -1)
            )
            characters_label.pack(anchor="nw", padx=106, pady=(0, 20))

            y_offset = 50  # Initial y_offset for the first character entry
            for character_id in non_victim_characters:
                character = characters_collection.find_one({"_id": character_id})

                background_label = Label(self.selection_canvas, image=self.background_image, bg="#202020", bd=0)
                background_label.place(x=80, y=y_offset - 15)

                icon_label = Label(self.selection_canvas, image=self.icon_image, bg="#292929", bd=0)
                icon_label.place(x=105, y=y_offset)

                text_label = Label(self.selection_canvas, text=f"{character['Name']} {character['Surname']}", bg="#292929", fg="#FFFFFF", font=("Inter", 13 * -1))
                text_label.place(x=189, y=y_offset)

                character_button = Canvas(
                    self.selection_canvas,
                    width=self.button_image.width(),
                    height=self.button_image.height(),
                    bg="#292929",
                    bd=0,
                    highlightthickness=0,
                    relief="flat"
                )
                character_button.create_image(0, 0, anchor="nw", image=self.button_image)
                character_button.place(x=916, y=y_offset - 3)

                character_button.bind(self.left_click, lambda e, char_id=character_id: self.select_character(char_id))

                y_offset += 70  # Increment y_offset for the next character entry

        if items:
            y_offset += 20

            items_label = Label(
                self.selection_canvas,
                text="Items",
                bg="#202020",
                fg="#D71D1D",
                font=(self.label_font, 24 * -1)
            )
            items_label.place(x=106, y=y_offset)

            y_offset += 60

            for item_id in items:
                item = items_collection.find_one({"_id": item_id})

                background_label = Label(self.selection_canvas, image=self.background_image, bg="#202020", bd=0)
                background_label.place(x=80, y=y_offset - 15)

                icon_label = Label(self.selection_canvas, image=self.icon_image, bg="#292929", bd=0)
                icon_label.place(x=105, y=y_offset)

                text_label = Label(self.selection_canvas, text=item['Name'], bg="#292929", fg="#FFFFFF", font=("Inter", 13 * -1))
                text_label.place(x=189, y=y_offset)

                item_button = Canvas(
                    self.selection_canvas,
                    width=self.button_image.width(),
                    height=self.button_image.height(),
                    bg="#292929",
                    bd=0,
                    highlightthickness=0,
                    relief="flat"
                )
                item_button.create_image(0, 0, anchor="nw", image=self.button_image)
                item_button.place(x=916, y=y_offset - 3)

                item_button.bind(self.left_click, lambda e, it_id=item_id: self.select_item(it_id))

                y_offset += 70

        button_canvas = Canvas(
            self.canvas,
            width=self.pressed_button_image.width(),
            height=self.pressed_button_image.height(),
            bg="#3D3D3D",
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        button_canvas.place(x=304.66650390625 - self.pressed_button_image.width() // 2, y=40.0 - self.pressed_button_image.height() // 2)
        button_canvas.create_image(0, 0, anchor="nw", image=self.pressed_button_image)

        button_canvas.bind(self.left_click, lambda event: self.display_locations())

        self.selection_canvas.update_idletasks()
        self.selection_canvas.config(scrollregion=self.selection_canvas.bbox("all"))

    def select_character(self, id, event=None):
        """
        Handle selection of a character.

        This method is triggered when a user selects a character from the UI,
        and it switches the interface to the chat screen for the selected character.

        Args:
        - id (str): The ID of the selected character.
        - event (Event, optional): The event object triggering the selection. Default is None.
        """
        self.switch_to_chat(self.day, id, type="Character")

    def select_item(self, id, event=None):
        """
        Handle selection of an item.

        This method is triggered when a user selects an item from the UI,
        and it switches the interface to the chat screen for the selected item.

        Args:
        - id (str): The ID of the selected item.
        - event (Event, optional): The event object triggering the selection. Default is None.
        """
        self.switch_to_chat(self.day, id, type="Item")

    def hide(self):
        """
        Hide the canvas.

        This method hides the main canvas element associated with the SelectScreen.
        """
        self.canvas.pack_forget()  # Hide canvas