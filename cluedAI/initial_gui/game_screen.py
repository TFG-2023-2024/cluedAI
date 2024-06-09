from pathlib import Path
from tkinter import BOTH, END, LEFT, RIGHT, Y, Frame, Scrollbar, Tk, Canvas, Entry, Button, PhotoImage
from initial_gui.reroll_screen import reroll

def chat():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/aya/Documents/tfg/cluedAI/cluedAI/initial_gui/assets/game")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)
    
    def reroll_response():
        if len(messages) >= 2:
            last_two_messages = [messages[-2][2], messages[-1][2]]  # Get the last two messages' text
            window.destroy()
            reroll(last_two_messages)
            
    
    window = Tk()
    window.geometry("1024x768")

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

    canvas.create_rectangle(0.0, 631.0, 1024.0, 768.0, fill="#292929", outline="")

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))

    button_canvas = Canvas(
        canvas,
        width=button_image_1.width(),
        height=button_image_1.height(),
        bg="#292929",
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    button_canvas.place(x=916.0, y=663.0)
    button_canvas.create_image(0, 0, anchor="nw", image=button_image_1)

    def create_rounded_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
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
        return messages_canvas.create_polygon(points, **kwargs, smooth=True)

    def display_message(message):
        y_offset = 10 if not messages else messages_canvas.bbox(messages[-1][1])[3] + 30  # Space between messages
        x_position = 960 - 12  # Adjust to fit within the messages_frame
        text_item = messages_canvas.create_text(x_position, y_offset, anchor="ne", text=message, fill="#FFFFFF", font=("Inter", 13 * -1))
        bbox = messages_canvas.bbox(text_item)
        padding = 10
        rect_x1 = bbox[0] - padding
        rect_y1 = bbox[1] - padding
        rect_x2 = bbox[2] + padding
        rect_y2 = bbox[3] + padding
        rounded_rect = create_rounded_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, radius=20, fill="#333333")
        messages_canvas.tag_lower(rounded_rect, text_item)
        messages.append((rounded_rect, text_item, message))

        # Update scroll region and scroll to the bottom
        messages_canvas.config(scrollregion=messages_canvas.bbox("all"))
        messages_canvas.yview_moveto(1.0)

    def submit_message(event=None):
        message = entry.get()
        if message:
            display_message(message)
            entry.delete(0, END)

    button_canvas.bind("<Button-1>", submit_message)

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(461.0, 698.5, image=entry_image_1)

    entry = Entry(
        bd=0,
        bg="#202020",
        fg="#FFFFFF",
        font=("Inter", 13 * -1),
        highlightthickness=0
    )

    def clear_default(event):
        event.widget.delete(0, 'end')
        event.widget.unbind('<FocusIn>')

    entry.insert(0, "Write your response here...")
    entry.bind('<FocusIn>', clear_default)
    entry.bind("<Return>", submit_message)
    entry.place(x=56.0, y=675.0, width=810.0, height=49.0)

    image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(510, 40, image=image_image_4)

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

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(304.66650390625, 40.0, image=image_image_2)

    button_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    
    button3_canvas = Canvas(
        canvas,
        width=button_image_3.width(),
        height=button_image_3.height(),
        bg="#3D3D3D",
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    button3_canvas.place(x=712.0 - button_image_3.width() // 2, y=40.0 - button_image_3.height() // 2)
    button3_canvas.create_image(0, 0, anchor="nw", image=button_image_3)
    
    button3_canvas.bind("<Button-1>", lambda event: reroll_response())  # Bind the left mouse click to the reroll function
    
    # Create the frame to hold the messages list and scrollbar
    messages_frame = Frame(window)
    messages_frame.place(x=0, y=100, width=1022, height=530)

    scrollbar = Scrollbar(messages_frame, orient="vertical")
    scrollbar.pack(side=RIGHT, fill=Y)

    messages_canvas = Canvas(messages_frame, bg="#202020", bd=0, highlightthickness=0, yscrollcommand=scrollbar.set)
    messages_canvas.pack(side=LEFT, fill=BOTH, expand=True)

    messages = []

    scrollbar.config(command=messages_canvas.yview)

    def on_mouse_wheel(event):
        messages_canvas.yview_scroll(-1 * event.delta, 'units')

    # Bind mouse wheel events for Windows and MacOS
    window.bind_all("<MouseWheel>", on_mouse_wheel)

    window.resizable(False, False)
    window.mainloop()