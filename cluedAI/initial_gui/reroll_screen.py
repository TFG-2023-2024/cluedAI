from pathlib import Path
from tkinter import (
    BOTH,
    END,
    LEFT,
    RIGHT,
    Y,
    Frame,
    Label,
    Scrollbar,
    Tk,
    Canvas,
    Entry,
    Button,
    PhotoImage,
)

def reroll(received_messages):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(
        r"assets/reroll_v0"
    )

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.geometry("1024x768")

    canvas = Canvas(
        window,
        bg="#202020",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge",
    )
    canvas.place(x=0, y=0)

    images = {}
    images["image_1"] = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(515.0, 403.0, image=images["image_1"])

    canvas.create_rectangle(0.0, 631.0, 1024.0, 768.0, fill="#292929", outline="")

    images["button_1"] = PhotoImage(file=relative_to_assets("button_1.png"))

    button_canvas = Canvas(
        canvas,
        width=images["button_1"].width(),
        height=images["button_1"].height(),
        bg="#292929",
        bd=0,
        highlightthickness=0,
        relief="ridge",
    )
    button_canvas.place(x=916.0, y=663.0)
    button_canvas.create_image(0, 0, anchor="nw", image=images["button_1"])

    def create_rounded_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return messages_canvas.create_polygon(points, **kwargs, smooth=True)

    def display_message(message):
        y_offset = (
            10 if not messages else messages_canvas.bbox(messages[-1][1])[3] + 30
        )  # Space between messages
        x_position = 960 - 12  # Adjust to fit within the messages_frame
        text_item = messages_canvas.create_text(
            x_position,
            y_offset,
            anchor="ne",
            text=message,
            fill="#FFFFFF",
            font=("Inter", 13 * -1),
        )
        bbox = messages_canvas.bbox(text_item)
        padding = 10
        rect_x1 = bbox[0] - padding
        rect_y1 = bbox[1] - padding
        rect_x2 = bbox[2] + padding
        rect_y2 = bbox[3] + padding
        rounded_rect = create_rounded_rectangle(
            rect_x1, rect_y1, rect_x2, rect_y2, radius=20, fill="#333333"
        )
        messages_canvas.tag_lower(rounded_rect, text_item)
        messages.append((rounded_rect, text_item, message))

        # Update scroll region and scroll to the bottom
        messages_canvas.config(scrollregion=messages_canvas.bbox("all"))
        messages_canvas.yview_moveto(1.0)

    def submit_reroll(event=None):
        message = entry.get()
        if message:
            display_message(message)  # no sirve aquí, cambiar a posteriori
            # GO BACK TO CHAT WITH REROLLED RESPONSE

    button_canvas.bind("<Button-1>", submit_reroll)

    images["entry_1"] = PhotoImage(file=relative_to_assets("entry_1.png"))
    canvas.create_image(461.0, 698.5, image=images["entry_1"])

    entry = Entry(
        bd=0, bg="#202020", fg="#FFFFFF", font=("Inter", 13 * -1), highlightthickness=0
    )

    def clear_default(event):
        event.widget.delete(0, "end")
        event.widget.unbind("<FocusIn>")

    entry.insert(0, "Write your response here...")
    entry.bind("<FocusIn>", clear_default)
    entry.bind("<Return>", submit_reroll)
    entry.place(x=56.0, y=675.0, width=810.0, height=49.0)

    images["image_4"] = PhotoImage(file=relative_to_assets("image_4.png"))
    canvas.create_image(510, 40, image=images["image_4"])

    # Create the "clued" text
    clued_text = canvas.create_text(
        454.0, 22.0, anchor="nw", text="Clued", fill="#F4F4F4", font=("Inter", 30 * -1)
    )

    # Calculate the width of the "clued" text
    clued_bbox = canvas.bbox(clued_text)
    clued_width = clued_bbox[2] - clued_bbox[0]

    # Create the "AI" text
    canvas.create_text(
        454.0
        + clued_width,  # Adjust x-coordinate to center "AI" text relative to "clued" text
        22.0,
        anchor="nw",
        text="AI",
        fill="#D71E1E",
        font=("Inter", 30 * -1),
    )

    images["image_2"] = PhotoImage(file=relative_to_assets("image_2.png"))
    canvas.create_image(304.66650390625, 40.0, image=images["image_2"])

    images["image_3"] = PhotoImage(file=relative_to_assets("image_3.png"))
    canvas.create_image(712.0, 40.0, image=images["image_3"])

    # Create the frame to hold the messages list and scrollbar
    messages_frame = Frame(window)
    messages_frame.place(x=0, y=100, width=1022, height=530)

    scrollbar = Scrollbar(messages_frame, orient="vertical")
    scrollbar.pack(side=RIGHT, fill=Y)

    messages_canvas = Canvas(
        messages_frame,
        bg="#202020",
        bd=0,
        highlightthickness=0,
        yscrollcommand=scrollbar.set,
    )
    messages_canvas.pack(side=LEFT, fill=BOTH, expand=True)

    messages = []

    scrollbar.config(command=messages_canvas.yview)

    def on_mouse_wheel(event):
        messages_canvas.yview_scroll(-1 * event.delta, "units")

    # Bind mouse wheel events for Windows and MacOS
    window.bind_all("<MouseWheel>", on_mouse_wheel)

    # Display the last two messages when the window opens
    for message in received_messages:
        print(message)
        display_message(message)

    # Create a canvas to hold the background image and text
    bg_text_canvas = Canvas(
        window,
        bg="#202020",
        height=55,
        width=835,
        bd=0,
        highlightthickness=0,
        relief="ridge",
    )
    bg_text_canvas.place(x=80, y=550)

    # Set the background image
    images["image_5"] = PhotoImage(file=relative_to_assets("image_5.png"))
    bg_text_canvas.create_image(0, 0, anchor="nw", image=images["image_5"])

    # Create the first text on the bg_text_canvas
    first_text = bg_text_canvas.create_text(
        55, 15, anchor="nw", text="This response will be ", fill="#FFFFFF", font=("Inter Bold", 18 * -1)
    )

    # Create the mid text on the bg_text_canvas
    mid_text = bg_text_canvas.create_text(
        bg_text_canvas.bbox(first_text)[2], 15, anchor="nw", text="rerolled.", fill="#D71E1E", font=("Inter Bold", 18 * -1)
    )

    # Create the end text on the bg_text_canvas
    bg_text_canvas.create_text(
        bg_text_canvas.bbox(mid_text)[2] + 1, 15, anchor="nw", text="Please write down the reason why you requested the reroll.", fill="#FFFFFF", font=("Inter Bold", 18 * -1)
    )

    window.resizable(False, False)
    window.mainloop()
