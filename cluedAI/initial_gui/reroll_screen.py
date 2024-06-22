from tkinter import Canvas, Entry, PhotoImage, Frame, Scrollbar, RIGHT, LEFT, Y, BOTH, END
from initial_gui.starting_operations import create_window, relative_to_assets


class RerollScreen:
    def __init__(self, root, switch_to_chat, day, response, id):
        """
        Initialize the RerollScreen instance.

        Args:
        - root (tk.Tk): The root Tk instance for the GUI.
        - switch_to_chat (callable): Function to switch to the chat screen for a specific ID.
        - day (int): The current day in the game.
        - response (tuple): A tuple containing two strings: message and response.
        - id (str): The ID associated with the chat screen (Character/Item).
        """
        self.root = root
        self.switch_to_chat = switch_to_chat
        self.day = day
        self.text_font = "Inter Bold"
        self.response = response
        self.id = id
        self.window, self.canvas = create_window("assets/reroll", existing_root=root)
        self.images = {}
        self.setup_ui()

    def load_images(self):
        """
        Load images required for the GUI.

        This method loads various images used in the GUI into the self.images dictionary.
        """
        images = {
            "bg": "bg.png",
            "msg_bg": "msg_bg.png",
            "entry_1": "entry_1.png",
            "banner": "banner.png",
            "calendar": "calendar.png",
            "pressed_button": "pressed_button.png",
            "button_1": "button_1.png"
        }

        for name, filename in images.items():
            self.images[name] = PhotoImage(file=relative_to_assets(filename))

    def setup_ui(self):
        """
        Set up the user interface for the RerollScreen.

        This method initializes the UI components including canvas, buttons, entry fields,
        header, message frames, and background text.
        """
        self.load_images()
        self.setup_canvas()
        self.setup_buttons()
        self.setup_entry()
        self.create_header()
        self.setup_message_frame()
        self.setup_bg_text()
        self.display_received()

    def setup_canvas(self):
        """
        Set up the canvas with background image and additional UI elements.

        This method configures the main canvas of the RerollScreen, setting a background image
        and creating necessary UI elements.
        """
        self.canvas.create_image(515.0, 390.0, image=self.images["bg"])
        self.canvas.create_rectangle(0.0, 631.0, 1024.0, 768.0, fill="#292929", outline="")

    def create_header(self):
        """
        Create the header section of the RerollScreen.

        This method constructs the header section with the game title, day indicator,
        and other decorative elements.
        """
        self.canvas.create_image(510, 40, image=self.images["banner"])
        self.canvas.create_image(712.0, 40.0, image=self.images["pressed_button"])

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

        self.canvas.create_image(38, 60.0 - self.images["calendar"].height() // 2, image=self.images["calendar"])

        self.day_label = self.canvas.create_text(
            31.0,
            28.0,
            anchor="nw",
            text=str(self.day),
            fill="#D71E1E",
            font=("Inter", 24)
        )   

    def setup_message_frame(self):
        """
        Set up the message frame with scrollable messages.

        This method creates a frame for displaying messages with a scrollbar for navigation.
        """
        messages_frame = Frame(self.window)
        messages_frame.place(x=32, y=100, width=990, height=530)

        self.scrollbar = Scrollbar(messages_frame, orient="vertical")
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.messages_canvas = Canvas(
            messages_frame,
            bg="#202020",
            bd=0,
            highlightthickness=0,
            yscrollcommand=self.scrollbar.set,
        )
        self.messages_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar.config(command=self.messages_canvas.yview)

        def on_mouse_wheel(event):
            self.messages_canvas.yview_scroll(-1 * event.delta, "units")

        self.window.bind_all("<MouseWheel>", on_mouse_wheel)

        self.messages = []
        self.responses = []

    def setup_entry(self):
        """
        Set up the entry field for user input.

        This method creates an entry field where users can input text for sending messages.
        """
        self.canvas.create_image(461.0, 698.5, image=self.images["entry_1"])

        self.entry = Entry(
            bd=0, bg="#202020", fg="#FFFFFF", font=("Inter", 13 * -1), highlightthickness=0
        )
        self.entry.insert(0, "Write your response here...")

        def clear_default(event):
            event.widget.delete(0, "end")
            event.widget.unbind("<FocusIn>")

        self.entry.bind("<FocusIn>", clear_default)
        self.entry.bind("<Return>", self.submit_reroll)
        self.entry.place(x=56.0, y=675.0, width=810.0, height=49.0)

    def setup_bg_text(self):
        """
        Set up the background text canvas.

        This method creates a canvas for displaying background text related to reroll requests.
        """
        bg_text_canvas = Canvas(
            self.window,
            bg="#202020",
            height=55,
            width=835,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        bg_text_canvas.place(x=80, y=550)
        bg_text_canvas.create_image(0, 0, anchor="nw", image=self.images["msg_bg"])

        first_text = bg_text_canvas.create_text(
            55, 15, anchor="nw", text="This response will be ", fill="#FFFFFF", font=(self.text_font, 18 * -1)
        )

        mid_text = bg_text_canvas.create_text(
            bg_text_canvas.bbox(first_text)[2], 15, anchor="nw", text="rerolled.", fill="#D71E1E", font=(self.text_font, 18 * -1)
        )

        bg_text_canvas.create_text(
            bg_text_canvas.bbox(mid_text)[2] + 1, 15, anchor="nw", text="Please write down the reason why you requested the reroll.", fill="#FFFFFF", font=(self.text_font, 18 * -1)
        )

    def setup_buttons(self):
        """
        Set up the buttons on the canvas.

        This method creates the reroll button for user interaction on the main canvas.
        """
        button_canvas = Canvas(
            self.canvas,
            width=self.images["button_1"].width(),
            height=self.images["button_1"].height(),
            bg="#292929",
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        button_canvas.place(x=916.0, y=663.0)
        button_canvas.create_image(0, 0, anchor="nw", image=self.images["button_1"])

        button_canvas.bind("<Button-1>", self.submit_reroll)

    def get_y_offset(self):
        """
        Calculate the y-offset for new messages or responses.

        This method calculates the vertical offset for placing new messages or responses
        based on the existing messages and responses in the messages_canvas.

        Returns:
        - int: The calculated y-offset.
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

    def display_received(self):
        """
        Display the received message and response on the canvas.

        This method displays the initial message and response received on the messages_canvas.
        """
        self.display_message(self.response[0])
        self.display_response(self.response[1])

    def display_message(self, message):
        """
        Display a message on the canvas with rounded rectangle.

        Args:
        - message (str): The message to display.
        """
        max_width = 960 - 12  # Adjust to fit within the messages_frame with some padding
        wrapped_message = self.wrap_text(self.messages_canvas, message, max_width)

        y_offset = self.get_y_offset()
        x_position = 960 - 30  # Adjust to fit within the messages_frame, ensuring right alignment

        # Create text item with anchor="ne" to align text to the right
        text_item = self.messages_canvas.create_text(
            x_position, y_offset, anchor="ne", text=wrapped_message, fill="#FFFFFF", font=("Inter", 13 * -1)
        )
        bbox = self.messages_canvas.bbox(text_item)
        padding = 10

        # Create bounding box for the rounded rectangle
        rect_x1 = bbox[0] - padding
        rect_y1 = bbox[1] - padding
        rect_x2 = bbox[2] + padding
        rect_y2 = bbox[3] + padding

        # Create the rounded rectangle
        rounded_rect = self.create_rounded_rectangle(
            rect_x1, rect_y1, rect_x2, rect_y2, radius=20, fill="#333333"
        )
        self.messages_canvas.tag_lower(rounded_rect, text_item)
        self.messages.append((rounded_rect, text_item, wrapped_message))

        # Update scroll region and scroll to the bottom
        self.messages_canvas.config(scrollregion=self.messages_canvas.bbox("all"))
        self.messages_canvas.yview_moveto(1.0)

    def display_response(self, response):
        """
        Display a response on the canvas with rounded rectangle.

        Args:
        - response (str): The response to display.
        """
        max_width = 960 - 60
        wrapped_response = self.wrap_text(self.messages_canvas, response, max_width)

        y_offset = self.get_y_offset()
        x_position = 30
        text_item = self.messages_canvas.create_text(x_position, y_offset, anchor="nw", text=wrapped_response, fill="#FFFFFF", font=("Inter", 13))
        bbox = self.messages_canvas.bbox(text_item)
        padding = 10
        rect_x1 = bbox[0] - padding
        rect_y1 = bbox[1] - padding
        rect_x2 = bbox[2] + padding
        rect_y2 = bbox[3] + padding
        rounded_rect = self.create_rounded_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, radius=20, fill="#D71E1E")
        self.messages_canvas.tag_lower(rounded_rect, text_item)
        
        # Update scroll region and scroll to the bottom
        self.messages_canvas.config(scrollregion=self.messages_canvas.bbox("all"))
        self.messages_canvas.yview_moveto(1.0)

    def wrap_text(self, canvas, text, max_width):
        """
        Wrap text to fit within max_width on the canvas.

        Args:
        - canvas (tk.Canvas): The canvas to wrap text on.
        - text (str): The text to wrap.
        - max_width (int): The maximum width to fit the text within.

        Returns:
        - str: The wrapped text.
        """
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            text_item = canvas.create_text(0, 0, anchor="nw", text=test_line, font=("Inter", 13 * -1))
            bbox = canvas.bbox(text_item)
            canvas.delete(text_item)

            if bbox[2] - bbox[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return "\n".join(lines)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        """
        Create a rounded rectangle on the canvas.

        Args:
        - x1 (int): X-coordinate of the top-left corner of the rectangle.
        - y1 (int): Y-coordinate of the top-left corner of the rectangle.
        - x2 (int): X-coordinate of the bottom-right corner of the rectangle.
        - y2 (int): Y-coordinate of the bottom-right corner of the rectangle.
        - radius (int): Radius of the rounded corners.
        - **kwargs: Additional keyword arguments for the rounded rectangle (e.g., fill color).

        Returns:
        - int: The ID of the created rounded rectangle on the canvas.
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

    def submit_reroll(self, event=None):
        """
        Handle submission of reroll message.

        Args:
        - event (tk.Event, optional): The event triggering the submission (e.g., button click).
        """
        message = self.entry.get()
        if message:
            self.entry.delete(0, END)
            self.switch_to_chat(self.day, self.id, type="Character", reroll=message)

    def hide(self):
        """
        Hide the RerollScreen canvas.

        This method hides the entire RerollScreen canvas.
        """
        self.canvas.pack_forget()  # Hide canvas
