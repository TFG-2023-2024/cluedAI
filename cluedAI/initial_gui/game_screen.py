from tkinter import BOTH, END, LEFT, RIGHT, Y, Frame, Scrollbar, Canvas, Entry, PhotoImage
import ai_operations as ai
from initial_gui.starting_operations import create_window, relative_to_assets
from dotenv import load_dotenv
from db.db_operations import obtain_by_id, connect_db
from db.db_operations import connect_db, start_day, start_day_0
from db.db_randomizers import randomize_archetypes

class ChatScreen:
    # Class variables to keep track of the cached data
    cached_day_data = None 
    cached_data = None
    cached_day = None
    cached_messages = []
    characters_spoken_to = {}
    
    def __init__(self, root, switch_to_select, switch_to_reroll, day, id, type, reroll=None):
        """
        Initialize the ChatScreen object.

        Parameters:
        - root: The root Tkinter window.
        - switch_to_select: Function to switch to the selection screen.
        - switch_to_reroll: Function to switch to the reroll screen.
        - day: The current day in the game.
        - id: Identifier for the character, item, or location.
        - type: Type of the object (Character, Item).
        - reroll: Optional, message to reroll.

        This method sets up the initial state of the ChatScreen object,
        including UI elements, database connections, and game data.
        """
        self.root = root
        self.switch_to_select = switch_to_select
        self.switch_to_reroll = switch_to_reroll
        self.day = day
        self.data = None
        self.reroll = reroll  
        self.id = id 
        self.type = type
        self.left_click = "<Button-1>"
        self.assistant = None
        self.response_submitted = False  # Flag to track if submit_response has been called

        load_dotenv()
        global characters_collection, items_collection, locations_collection
        _, characters_collection, items_collection, locations_collection, _, _ = connect_db()

        self.window, self.canvas = create_window("assets/game", existing_root=root)

        # Initialize messages and responses lists
        self.messages = []
        self.responses = []

        # Initialize UI components
        self.initialize_ui()
    
    def initialize_ui(self):
        """
        Initialize the user interface components based on the current day.

        This method loads necessary data, checks if the character has been spoken to today,
        creates or obtains a thread for communication, loads images, and sets up UI elements
        like buttons, entry field, and message frames.
        """
        if self.day == 1:
            if ChatScreen.cached_day_data is None:
                ChatScreen.cached_day_data = start_day()
            self.data = ChatScreen.cached_day_data

       # Check if the character has been spoken to today
        if self.day in ChatScreen.characters_spoken_to:
            spoken_to_today = any(char[0] == self.id for char in ChatScreen.characters_spoken_to[self.day])
        else:
            spoken_to_today = False
        if spoken_to_today:
            self.thread = ai.obtain_thread_by_id(ChatScreen.characters_spoken_to[self.day][0][1])
        else:
            self.thread = ai.create_thread()
            if self.day not in ChatScreen.characters_spoken_to:
                ChatScreen.characters_spoken_to[self.day] = []
            ChatScreen.characters_spoken_to[self.day].append([self.id, self.thread.id])

        self.load_images()  # Load all images
        self.create_background()
        self.create_buttons()
        self.create_entry()
        self.create_header()
        self.create_message_frame()
        self.end_game()
        self.start_game()
        self.summarize()
        self.process_reroll()

    def process_reroll(self):
        """
        Process reroll if there is a reroll message available.

        This method checks if there is a reroll message and calls the AI function to reroll 
        the response. If a reroll response is received, it is displayed on the UI.
        """
        if self.reroll:
            reroll_message = self.reroll
            reroll_response = ai.reroll(self.id, self.thread, reroll_message)
            if reroll_response:
                self.display_responses(reroll_response)

    def start_game(self):
        """
        Start the game and display the tutorial for the first day.

        This method initializes the game environment, creates a new thread, blocks the button 
        until the tutorial is finished, and displays a welcome message followed by a tutorial 
        message to guide the player.
        """
        if self.day == 0:
            self.thread = ai.create_thread()
            self.block_button()

            welcome_message = ("Welcome to CluedAI, an AI-based murder mystery game created for a thesis project." + 
                               " In this game, you will chat with various characters to work through the mystery.")
            self.display_responses(welcome_message)
            self.root.after(3000, self.display_tutorial)

    def display_tutorial(self):
        """
        Display the tutorial message to guide the player.

        This method informs the player about interacting with buttons, message limits, and starting 
        the story. After displaying the tutorial, it unblocks the button for interaction.
        """
        tutorial_message = ("You can interact with the environment using buttons. " +
                            "The left button is used to select a location, character, or item, while the right button allows you to reroll a response. " +
                            "You have 10 messages per day. Use them wisely to uncover the truth. " +
                            "If you understand, write something and press the send button to start your story!")
        self.display_responses(tutorial_message)
        self.unblock_button()

    def complete_tutorial(self):
        """
        Complete the tutorial and start the game.

        This method randomizes character archetypes, retrieves initial game data, and starts the 
        story based on the current day. It also provides information about characters, items, and 
        locations to the AI to initiate the game's narrative.
        """
        randomize_archetypes(characters_collection)
        # Call start_day or start_day_0 based on the current day
        if self.day == 0:
            if ChatScreen.cached_day_data is None:
                ChatScreen.cached_day_data = start_day_0()
            self.data = ChatScreen.cached_day_data
        
        all_characters = characters_collection.find()
        characters_info = "Characters:\n" + "\n".join([f"Name: {character['Name']}, Role: {character['Archetype']}, " + 
            f"Location: {character['Location']}" for character in all_characters])

        all_items = items_collection.find()
        items_info = "Items:\n" + "\n".join([f"Name: {item['Name']}, Description: {item['Definition']}, " + 
                        f"Location: {item['Location']}" for item in all_items])

        all_locations = locations_collection.find()
        locations_info = "Locations:\n" + "\n".join([f"Room: {location['Room']}, Description: {location['Description']}" for location in all_locations])

        information = f"{characters_info}\n\n{items_info}\n\n{locations_info}"
        starting_message = ai.start_story(information)
        self.display_responses(starting_message)
        
    def block_button(self):
        """
        Block the interaction with buttons.

        This method disables the interaction with buttons to prevent unintended user actions 
        during specific game phases or tutorials.
        """
        self.submit_button_canvas.unbind(self.left_click)
        self.button2_canvas.unbind(self.left_click)
        self.button3_canvas.unbind(self.left_click)

    def unblock_button(self):
        """
        Unblock the interaction with buttons.

        This method enables the interaction with buttons after specific game phases or tutorials 
        are completed, allowing the user to proceed with their actions.
        """
        self.submit_button_canvas.bind(self.left_click, self.submit_message)

    def load_images(self):
        """
        Load all images required for the game UI.

        This method loads various images used in the game interface, such as backgrounds, buttons, 
        and icons, into PhotoImage objects for display on the canvas.
        """
        self.image_bg = PhotoImage(file=relative_to_assets("bg.png"))
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.button_select_button = PhotoImage(file=relative_to_assets("select_button.png"))
        self.button_reroll_button = PhotoImage(file=relative_to_assets("reroll_button.png"))
        self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.banner_image = PhotoImage(file=relative_to_assets("banner.png"))
        self.calendar_image = PhotoImage(file=relative_to_assets("calendar.png"))

    def create_background(self):
        """
        Create and display the game background.

        This method creates the main background image and a rectangle overlay for the game canvas, 
        providing a visual backdrop for the game UI elements.
        """
        self.canvas.create_image(515.0, 390.0, image=self.image_bg)
        self.canvas.create_rectangle(0.0, 631.0, 1024.0, 768.0, fill="#292929", outline="")

    def create_buttons(self):
        """
        Create and initialize the UI buttons for submitting, selecting, and rerolling.

        This method creates three Canvas objects for buttons: submit_button_canvas,
        button2_canvas (select button), and button3_canvas (reroll button). Each Canvas
        is configured with specific attributes such as size, background color, and image,
        and their click events are bound to corresponding functions.
        """
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

        self.button2_canvas = Canvas(
            self.canvas,
            width=self.button_select_button.width(),
            height=self.button_select_button.height(),
            bg="#3D3D3D",
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.button2_canvas.place(x=304.66650390625 - self.button_select_button.width() // 2, y=40.0 - self.button_select_button.height() // 2)
        self.button2_canvas.create_image(0, 0, anchor="nw", image=self.button_select_button)
        self.button2_canvas.bind(self.left_click, lambda event: self.select())

        self.button3_canvas = Canvas(
            self.canvas,
            width=self.button_reroll_button.width(),
            height=self.button_reroll_button.height(),
            bg="#3D3D3D",
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.button3_canvas.place(x=712.0 - self.button_reroll_button.width() // 2, y=40.0 - self.button_reroll_button.height() // 2)
        self.button3_canvas.create_image(0, 0, anchor="nw", image=self.button_reroll_button)
        self.button3_canvas.bind(self.left_click, lambda event: self.reroll_response())

    def create_entry(self):
        """
        Create and initialize the text entry field for user messages.

        This method creates an Entry widget for user input, setting its appearance
        and initial text. It also binds events for focus and return (Enter key)
        to corresponding functions for clearing default text and submitting messages.
        """
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
        """
        Create and initialize the game header with title and day indicator.

        This method creates a header displaying the game title "CluedAI", the current day,
        and other relevant icons (e.g., calendar). It uses Canvas and Text widgets for
        rendering text and images onto the game canvas.
        """
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
        """
        Create and initialize the message frame for displaying chat history.

        This method sets up a scrollable message frame using a Frame widget within the main
        game window. It includes a Canvas for displaying messages with a scrollbar for
        navigation. Mouse wheel events are bound to scroll through messages.
        """
        if self.day == 0 or self.day == 5 or self.reroll:
            messages_frame = Frame(self.window)
            messages_frame.place(x=20, y=100, width=1002, height=530)
        else:
            messages_frame = Frame(self.window)
            messages_frame.place(x=0, y=100, width=1022, height=530)

        scrollbar = Scrollbar(messages_frame, orient="vertical")
        scrollbar.pack(side=RIGHT, fill=Y)

        self.messages_canvas = Canvas(messages_frame, bg="#202020", bd=0, highlightthickness=0, yscrollcommand=scrollbar.set)
        self.messages_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar.config(command=self.messages_canvas.yview)

        self.root.bind_all("<MouseWheel>", self.on_mouse_wheel)  # Bind mouse wheel events

    def wrap_text(self, text, max_width):
        """
        Wrap text to fit within a maximum width.

        This method breaks down a long text string into multiple lines to fit within a specified
        maximum width, ensuring it doesn't exceed the width of the message canvas.
        """
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
        """
        Reset chat interface for a new day or game session.

        This method resets the chat interface by incrementing the day count,
        clearing displayed messages and responses, and preparing for a new
        interaction session or tutorial.
        """
        self.day += 1
        self.canvas.itemconfig(self.day_label, text=str(self.day))
        
        if self.day > 1 and self.day != 5:
            if ChatScreen.cached_day_data is None or ChatScreen.cached_day != self.day:
                ChatScreen.cached_day_data = start_day()
                ChatScreen.cached_messages.clear()
                ChatScreen.cached_day = self.day
            self.data = ChatScreen.cached_day_data
        
        if self.day == 5:
            self.switch_to_select(self.day, self.data)

        for item in self.messages + self.responses:
            self.messages_canvas.delete(item[0])
            self.messages_canvas.delete(item[1])
        
        self.messages.clear()
        self.responses.clear()
        self.messages_canvas.config(scrollregion=self.messages_canvas.bbox("all"))
        self.root.after(100, lambda: self.switch_to_select(self.day, self.data))  # 100 ms delay

    def get_y_offset(self):
        """
        Calculate the vertical offset for positioning new messages or responses.

        This method calculates the vertical position offset based on the last displayed
        message or response in the chat interface, ensuring new content is displayed
        below the previous one without overlapping.
        """
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
        """
        Display a user message in the chat interface.

        This method formats and displays a message within the chat message frame,
        wrapping the text if necessary to fit within the message canvas.
        """
        max_width = 960 - 60
        wrapped_message = self.wrap_text(message, max_width)

        y_offset = self.get_y_offset()
        if self.day == 0 or self.day == 5 or self.reroll: 
            x_position = 970
        else:
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
        ChatScreen.cached_messages.append(message)

        self.messages_canvas.config(scrollregion=self.messages_canvas.bbox("all"))
        self.messages_canvas.yview_moveto(1.0)

        if len(self.responses) == 10 or len(ChatScreen.cached_messages) == 10:
            self.responses.clear()
            ChatScreen.cached_messages.clear()
            self.block_button()
            self.root.after(2000, self.display_day_over_message)

    def display_day_over_message(self):
        """
        Display a message indicating the day is over and schedule a reset of the chat after 5 seconds.
        """
        self.display_responses("DAY OVER, continuing in 5 seconds...")
        self.unblock_button()
        self.root.after(5000, self.reset_chat)

    def display_responses(self, response):
        """
        Display a response message on the messages canvas with wrapping and styling.

        Args:
        - response (str): The response message to display.
        """
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

        if self.day == 0:
            self.button2_canvas.bind(self.left_click, lambda event: self.select())
            self.button3_canvas.bind(self.left_click, lambda event: self.reroll_response())


    def summarize(self):
        """
        Summarize the conversation based on the character's type and day.
        """
        if self.type != "Character" or self.responses:
            return
        
        self.assistant = ai.create_assistant(self.id)
        if self.day == 1:
            ai.obtain_summary(self.assistant, self.thread, self.day)
        else:
            self.summarize_other_days()

    def summarize_other_days(self):
        """
        Summarize the conversation for days other than day 1.

        This method iterates through the previous days' conversations and
        summarizes based on the character's ID.
        """
        new_talk = True
        all_days = sorted(ChatScreen.characters_spoken_to.keys(), reverse=True)
        all_days.pop(0)
        for clave in all_days:
            for sublist in ChatScreen.characters_spoken_to[clave]:
                if sublist[0] == self.id:
                    thread = ai.obtain_thread_by_id(sublist[1])
                    ai.obtain_summary(self.assistant, thread, self.day, self.thread)
                    new_talk = False
                    break
        if new_talk:
            ai.obtain_summary(self.assistant, self.thread, self.day)

    def end_game(self):
        """
        End the game and display final responses. Close the game after a delay if it's the last day.
        """
        if self.day != 5:
            return
        
        self.block_button()
        all_characters = characters_collection.find()
        characters_info = [f"Name: {character['Name']}, Role: {character['Archetype']}" for character in all_characters]
        
        response = ai.end_story(characters_info, self.id)
        self.display_responses(response)
        
        def after_first_response():
            self.display_responses("Thank you for playing cluedAI. The game will close in 30 seconds...")
            self.root.after(30000, self.destroy)
        
        self.root.after(10000, after_first_response)

    def submit_message(self, event=None):
        """
        Submit a message entered in the entry widget.

        Args:
        - event (tk.Event, optional): The event triggering the submission, like pressing Enter. Defaults to None.
        """
        message = self.entry.get()
        if message:
            self.display_message(message)
            self.entry.delete(0, END)
            if self.day > 0:
                self.submit_response(message)
            else:
                wait_msg = "Please wait a few seconds to start..."
                self.submit_button_canvas.unbind(self.left_click)
                self.submit_response(wait_msg)
                self.root.after(2000, self.complete_tutorial)
                
    def clear_default(self, event):
        """
        Clear the default text in the entry widget when it gains focus.

        Args:
        - event (tk.Event): The event object associated with the focus gain.
        """
        event.widget.delete(0, 'end')
        event.widget.unbind('<FocusIn>')

    def reroll_response(self, event=None):
        """
        Reroll the last response if there is at least one response available.

        Args:
        - event (tk.Event, optional): The event triggering the reroll, such as a button click. Defaults to None.
        """
        if len(self.responses) >= 1:
            last_messages = [self.messages[-1][2], self.responses[-1][2]]
            self.switch_to_reroll(self.day, last_messages, self.id)

    def submit_response(self, message):
        """
        Submit a response to the chat interface based on the type of conversation.

        Args:
        - message (str): The response message to submit.
        """
        if self.id:
            if self.type=="Character":
                response = ai.chat_by_thread(self.assistant, self.thread, message)
            elif self.type=="Item":
                response = ai.chat_narrator("Item", str(obtain_by_id(self.id, items_collection)), message)
        else:
            if self.responses and not self.response_submitted:
                self.response_submitted = True
            response = message
        if response:
            self.display_responses(response)

    def on_mouse_wheel(self, event):
        """
        Scroll the messages canvas in response to mouse wheel events.

        Args:
        - event (tk.Event): The mouse wheel event object.
        """
        self.messages_canvas.yview_scroll(-1 * event.delta, 'units')

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        """
        Create a rounded rectangle on the messages canvas.

        Args:
        - x1 (int): X-coordinate of the top-left corner of the rectangle.
        - y1 (int): Y-coordinate of the top-left corner of the rectangle.
        - x2 (int): X-coordinate of the bottom-right corner of the rectangle.
        - y2 (int): Y-coordinate of the bottom-right corner of the rectangle.
        - radius (int, optional): Corner radius of the rounded rectangle. Defaults to 25.
        - **kwargs: Additional keyword arguments for styling the rounded rectangle.

        Returns:
        - int: The item id of the created rounded rectangle on the canvas.
        """
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
    
    def select(self):
        """
        Select an option based on the current day. Resets the chat if it's day 0.
        """
        if self.day == 0:
            self.reset_chat()
            self.root.after(100, lambda: self.switch_to_select(self.day, self.data))  # 100 ms delay
        else:
            self.switch_to_select(self.day, self.data)

    def hide(self):
        """
        Hide the canvas.
        """
        self.canvas.pack_forget()