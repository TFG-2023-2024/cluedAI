from tkinter import BOTH, END, LEFT, RIGHT, Y, Frame, Scrollbar, Canvas, Entry, Button, PhotoImage, Tk
import ai_operations as ai
from initial_gui.starting_operations import create_window, relative_to_assets
from dotenv import load_dotenv
from db.db_operations import obtain_by_id, connect_db
from db.db_operations import connect_db, start_day, start_day_0
from db.db_randomizers import randomize_archetypes

class ChatScreen:
    def __init__(self, root, switch_to_select, switch_to_reroll, day, id, type, reroll=None):
        self.root = root
        self.switch_to_select = switch_to_select
        self.switch_to_reroll = switch_to_reroll
        self.day = day
        self.data = None
        self.reroll = reroll  # Store reroll data if provided
        self.id = id  # Store id if provided
        self.type = type
        self.left_click = "<Button-1>"
        self.hilo = ai.create_thread()
        self.assistant = None

        load_dotenv()
        global characters_collection, items_collection, locations_collection
        _, characters_collection, items_collection, locations_collection, _, _ = connect_db()

        # Create window and canvas
        self.window, self.canvas = create_window("assets/game", existing_root=root)

        # Initialize messages and responses lists
        self.messages = []
        self.responses = []

        # Initialize UI components
        self.initialize_ui()
    
    def initialize_ui(self):
        # Call start_day or start_day_0 based on the current day
        if self.day == 0:
            self.data = start_day_0()
        elif self.day > 1:
            self.data = start_day()

        self.load_images()  # Load all images
        self.create_background()
        self.create_buttons()
        self.create_entry()
        self.create_header()
        self.create_message_frame()
        self.start_game()
        self.process_reroll()

    def process_reroll(self):
        if self.reroll:
            reroll_message = self.reroll
            reroll_response = ai.reroll(self.id, self.hilo, reroll_message)
            if reroll_response:
                self.display_responses(reroll_response)

    def start_game(self):
        if self.day == 0:
            # Block the button until the tutorial finishes
            self.block_button()

            # Display welcome message
            welcome_message = ("Welcome to CluedAI, an AI-based murder mystery game created for a thesis project." + 
                               " In this game, you will chat with various characters to uncover the mystery.")
            self.display_responses(welcome_message)
            self.root.after(3000, self.display_tutorial)

    def display_tutorial(self):
        tutorial_message = ("In this game, you can interact with the environment using buttons. " +
                            "The left button is used to select a location, character, or item, while the right button allows you to reroll a response." +
                            "If you understand, write something and press the send button to start your story!")
        self.display_responses(tutorial_message)
        # Unblock the button after the tutorial finishes
        self.unblock_button()

    def complete_tutorial(self):
        randomize_archetypes(characters_collection)
        
        # Collect all characters
        all_characters = characters_collection.find()
        characters_info = "Characters:\n" + "\n".join([f"Name: {character['Name']}, Role: {character['Archetype']}" for character in all_characters])

        # Collect all items
        all_items = items_collection.find()
        items_info = "Items:\n" + "\n".join([f"Name: {item['Name']}, Description: {item['Definition']}" for item in all_items])

        # Collect all locations
        all_locations = locations_collection.find()
        locations_info = "Locations:\n" + "\n".join([f"Room: {location['Room']}, Description: {location['Description']}" for location in all_locations])

        # Concatenate all information into one string
        information = f"{characters_info}\n\n{items_info}\n\n{locations_info}"

        starting_message = ai.start_story(information)
        self.display_responses(starting_message)
        
    def block_button(self):
        # Block the button (disable interaction)
        self.submit_button_canvas.config(state="disabled")

    def unblock_button(self):
        # Unblock the button (enable interaction)
        self.submit_button_canvas.config(state="normal")

    def load_images(self):
        self.image_bg = PhotoImage(file=relative_to_assets("bg.png"))
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.button_select_button = PhotoImage(file=relative_to_assets("select_button.png"))
        self.button_reroll_button = PhotoImage(file=relative_to_assets("reroll_button.png"))
        self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.banner_image = PhotoImage(file=relative_to_assets("banner.png"))
        self.calendar_image = PhotoImage(file=relative_to_assets("calendar.png"))

    def create_background(self):
        self.canvas.create_image(515.0, 390.0, image=self.image_bg)
        self.canvas.create_rectangle(0.0, 631.0, 1024.0, 768.0, fill="#292929", outline="")

    def create_buttons(self):
        self.submit_button_canvas = Canvas(
            self.canvas,
            width=self.button_image_1.width(),
            height=self.button_image_1.height(),
            bg="#292929",
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.submit_button_canvas.place(x=916.0, y=663.0)
        self.submit_button_canvas.create_image(0, 0, anchor="nw", image=self.button_image_1)
        self.submit_button_canvas.bind(self.left_click, self.submit_message)

        button2_canvas = Canvas(
            self.canvas,
            width=self.button_select_button.width(),
            height=self.button_select_button.height(),
            bg="#3D3D3D",
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        button2_canvas.place(x=304.66650390625 - self.button_select_button.width() // 2, y=40.0 - self.button_select_button.height() // 2)
        button2_canvas.create_image(0, 0, anchor="nw", image=self.button_select_button)
        button2_canvas.bind(self.left_click, lambda event: self.select(self.day, self.data))

        button3_canvas = Canvas(
            self.canvas,
            width=self.button_reroll_button.width(),
            height=self.button_reroll_button.height(),
            bg="#3D3D3D",
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        button3_canvas.place(x=712.0 - self.button_reroll_button.width() // 2, y=40.0 - self.button_reroll_button.height() // 2)
        button3_canvas.create_image(0, 0, anchor="nw", image=self.button_reroll_button)
        button3_canvas.bind(self.left_click, lambda event: self.reroll_response())

    def create_entry(self):
        self.canvas.create_image(461.0, 698.5, image=self.entry_image_1)

        self.entry = Entry(
            self.canvas,
            bd=0,
            bg="#202020",
            fg="#FFFFFF",
            font=("Inter", 13),
            highlightthickness=0
        )
        self.entry.insert(0, "Write your response here...")
        self.entry.bind('<FocusIn>', self.clear_default)
        self.entry.bind("<Return>", self.submit_message)
        self.entry.place(x=56.0, y=675.0, width=810.0, height=49.0)

    def create_header(self):
        self.canvas.create_image(510, 40, image=self.banner_image)

        clued_text = self.canvas.create_text(
            454.0,
            22.0,
            anchor="nw",
            text="Clued",
            fill="#F4F4F4",
            font=("Inter", 30)
        )

        clued_bbox = self.canvas.bbox(clued_text)
        clued_width = clued_bbox[2] - clued_bbox[0]

        self.canvas.create_text(
            454.0 + clued_width,
            22.0,
            anchor="nw",
            text="AI",
            fill="#D71E1E",
            font=("Inter", 30)
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

    def create_message_frame(self):
        messages_frame = Frame(self.window)
        messages_frame.place(x=0, y=100, width=1022, height=530)

        scrollbar = Scrollbar(messages_frame, orient="vertical")
        scrollbar.pack(side=RIGHT, fill=Y)

        self.messages_canvas = Canvas(messages_frame, bg="#202020", bd=0, highlightthickness=0, yscrollcommand=scrollbar.set)
        self.messages_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar.config(command=self.messages_canvas.yview)

        self.root.bind_all("<MouseWheel>", self.on_mouse_wheel)  # Bind mouse wheel events

    def wrap_text(self, text, max_width):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            text_item = self.messages_canvas.create_text(0, 0, anchor="nw", text=test_line, font=("Inter", 13))
            bbox = self.messages_canvas.bbox(text_item)
            self.messages_canvas.delete(text_item)

            if bbox[2] - bbox[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return "\n".join(lines)

    def reset_chat(self):
        self.day += 1
        self.canvas.itemconfig(self.day_label, text=str(self.day))
        
        #if self.day > 0: #ARREGLAR
            #ai.obtain_summary(self.assistant, self.hilo)
        
        if self.day == 7:
            self.switch_to_select(self.day, self.data)

        for item in self.messages + self.responses:
            self.messages_canvas.delete(item[0])
            self.messages_canvas.delete(item[1])

        self.messages.clear()
        self.responses.clear()
        self.messages_canvas.config(scrollregion=self.messages_canvas.bbox("all"))

    def get_y_offset(self):
        if not self.messages and not self.responses:
            return 10
        last_message_bbox = self.messages_canvas.bbox(self.messages[-1][1]) if self.messages else None
        last_response_bbox = self.messages_canvas.bbox(self.responses[-1][1]) if self.responses else None

        if last_message_bbox and last_response_bbox:
            return max(last_message_bbox[3], last_response_bbox[3]) + 30
        elif last_message_bbox:
            return last_message_bbox[3] + 30
        elif last_response_bbox:
            return last_response_bbox[3] + 30
        return 10

    def display_message(self, message):
        max_width = 960 - 60
        wrapped_message = self.wrap_text(message, max_width)

        y_offset = self.get_y_offset()
        x_position = 960 - 12
        text_item = self.messages_canvas.create_text(x_position, y_offset, anchor="ne", text=wrapped_message, fill="#FFFFFF", font=("Inter", 13))
        bbox = self.messages_canvas.bbox(text_item)
        padding = 10
        rect_x1 = bbox[0] - padding
        rect_y1 = bbox[1] - padding
        rect_x2 = bbox[2] + padding
        rect_y2 = bbox[3] + padding
        rounded_rect = self.create_rounded_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, radius=20, fill="#333333")
        self.messages_canvas.tag_lower(rounded_rect, text_item)
        self.messages.append((rounded_rect, text_item, wrapped_message))

        self.messages_canvas.config(scrollregion=self.messages_canvas.bbox("all"))
        self.messages_canvas.yview_moveto(1.0)

        if len(self.messages) + len(self.responses) >= 20:
            self.reset_chat()

    def display_responses(self, response):
        max_width = 960 - 60
        wrapped_response = self.wrap_text(''.join(response), max_width)

        y_offset = self.get_y_offset()
        x_position = 40
        text_item = self.messages_canvas.create_text(x_position, y_offset, anchor="nw", text=wrapped_response, fill="#FFFFFF", font=("Inter", 13))
        bbox = self.messages_canvas.bbox(text_item)
        padding = 10
        rect_x1 = bbox[0] - padding
        rect_y1 = bbox[1] - padding
        rect_x2 = bbox[2] + padding
        rect_y2 = bbox[3] + padding
        rounded_rect = self.create_rounded_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, radius=20, fill="#D71E1E")
        self.messages_canvas.tag_lower(rounded_rect, text_item)
        self.responses.append((rounded_rect, text_item, wrapped_response))

        self.messages_canvas.config(scrollregion=self.messages_canvas.bbox("all"))
        self.messages_canvas.yview_moveto(1.0)

        if len(self.messages) + len(self.responses) >= 20:
            self.reset_chat()

    def submit_message(self, event=None):
        message = self.entry.get()
        if message:
            self.display_message(message)
            self.entry.delete(0, END)
            if self.day > 0:
                self.submit_response(message)
            else:
                wait_msg = "Please wait a few seconds to start..."
                self.submit_response(wait_msg)
                self.root.after(2000, self.complete_tutorial)
                

    def clear_default(self, event):
        event.widget.delete(0, 'end')
        event.widget.unbind('<FocusIn>')

    def reroll_response(self, event=None):
        if len(self.responses) >= 1:
            last_messages = [self.messages[-1][2], self.responses[-1][2]]
            self.switch_to_reroll(self.day, last_messages, self.id)

    def submit_response(self, message):
        if self.id:
            if self.type=="Character":
                self.assistant = ai.create_assistant(self.id)
                response = ai.chat_by_thread(self.assistant, self.hilo, message)
            elif self.type=="Item":
                response = ai.chat_narrator("Item", str(obtain_by_id(self.id, items_collection)), message)
        else:
            response = message
        if response:
            self.display_responses(response)

    def on_mouse_wheel(self, event):
        self.messages_canvas.yview_scroll(-1 * event.delta, 'units')

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.messages_canvas.create_polygon(points, **kwargs, smooth=True)
    
    def select(self, day, data):
        if day == 0:
            self.reset_chat()
        self.switch_to_select(day, data)

    def hide(self):
        self.canvas.pack_forget()  # Hide canvas