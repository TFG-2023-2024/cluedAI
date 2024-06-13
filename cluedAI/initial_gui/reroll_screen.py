from tkinter import Tk, Canvas, Entry, PhotoImage, Frame, Scrollbar, RIGHT, LEFT, Y, BOTH, END
from initial_gui.starting_operations import create_window, relative_to_assets


class RerollScreen:
    def __init__(self, root, switch_to_chat, day, response):
        self.root = root
        self.switch_to_chat = switch_to_chat
        self.day = day
        self.text_font = "Inter Bold"
        self.response = response
        self.window, self.canvas = create_window("assets/reroll", existing_root=root)

        self.images = {}

        self.setup_ui()

    def load_images(self):
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
        self.load_images()
        self.setup_canvas()
        self.setup_buttons()
        self.setup_entry()
        self.create_header()
        self.setup_message_frame()
        self.setup_bg_text()
        self.display_response()

    def setup_canvas(self):
        # Set background image
        self.canvas.create_image(515.0, 390.0, image=self.images["bg"])
        self.canvas.create_rectangle(0.0, 631.0, 1024.0, 768.0, fill="#292929", outline="")

    def create_header(self):
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

    def setup_entry(self):
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
        # Create a canvas to hold the background image and text
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

        # Set the background image
        bg_text_canvas.create_image(0, 0, anchor="nw", image=self.images["msg_bg"])

        # Create the first text on the bg_text_canvas
        first_text = bg_text_canvas.create_text(
            55, 15, anchor="nw", text="This response will be ", fill="#FFFFFF", font=(self.text_font, 18 * -1)
        )

        # Create the mid text on the bg_text_canvas
        mid_text = bg_text_canvas.create_text(
            bg_text_canvas.bbox(first_text)[2], 15, anchor="nw", text="rerolled.", fill="#D71E1E", font=(self.text_font, 18 * -1)
        )

        # Create the end text on the bg_text_canvas
        bg_text_canvas.create_text(
            bg_text_canvas.bbox(mid_text)[2] + 1, 15, anchor="nw", text="Please write down the reason why you requested the reroll.", fill="#FFFFFF", font=(self.text_font, 18 * -1)
        )

    def setup_buttons(self):
        # Create the reroll button
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

    def display_response(self):
        # Display any received messages initially
        for message in self.response:
            self.display_message(message)

    def display_message(self, message):
        # Display a new message in the messages_canvas
        max_width = 960 - 12  # Adjust to fit within the messages_frame with some padding
        wrapped_message = self.wrap_text(self.messages_canvas, message, max_width)

        y_offset = 10 if not self.messages else self.messages_canvas.bbox(self.messages[-1][1])[3] + 30  # Space between messages
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

    def wrap_text(self, canvas, text, max_width):
        # Wrap text to fit within max_width on the canvas
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
        # Helper function to create a rounded rectangle
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
        # Handle submission of reroll message
        message = self.entry.get()
        if message:
            self.display_message(message)
            self.entry.delete(0, END)
            self.switch_to_chat()  # Example function call to switch back to chat screen

    def hide(self):
        self.canvas.pack_forget()  # Hide canvas
