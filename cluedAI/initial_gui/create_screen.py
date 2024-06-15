from tkinter import Entry, Button, PhotoImage, messagebox
from initial_gui.starting_operations import create_window, relative_to_assets
from users.user_operations import insert_character

class CreateScreen:
    def __init__(self, root, switch_to_chat, username):
        self.root = root
        self.switch_to_chat = switch_to_chat
        self.username = username
        self.window, self.canvas = create_window("assets/create", existing_root=root)
        self.focus = '<FocusIn>'
        self.image_refs = {}  # Initialize image reference dictionary

    def show(self):
        self.load_images()
        self.create_ui_elements()

    def load_images(self):
        try:
            self.image_refs["bg"] = PhotoImage(file=relative_to_assets("bg.png"))
            self.image_refs["banner"] = PhotoImage(file=relative_to_assets("banner.png"))
            self.image_refs["divider"] = PhotoImage(file=relative_to_assets("divider.png"))
            self.image_refs["entry_bg_1"] = PhotoImage(file=relative_to_assets("entry_bg_1.png"))
            self.image_refs["entry_1"] = PhotoImage(file=relative_to_assets("entry_1.png"))
            self.image_refs["entry_bg_2"] = PhotoImage(file=relative_to_assets("entry_bg_2.png"))
            self.image_refs["entry_2"] = PhotoImage(file=relative_to_assets("entry_2.png"))
            self.image_refs["icon"] = PhotoImage(file=relative_to_assets("icon.png"))
            self.image_refs["submit_button"] = PhotoImage(file=relative_to_assets("submit_button.png"))
        except Exception as e:
            print(f"Error loading images: {e}")  # Print any error loading images for debugging

    def create_ui_elements(self):
        self.canvas.create_image(515.0, 390.0, image=self.image_refs["bg"])

        self.canvas.create_text(427.0, 142.0, anchor="nw", text="Create your own character!", fill="#7B7B7B", font=("Inter Light", 13))

        # Create the "clued" text
        clued_text = self.canvas.create_text(415.0, 69.0, anchor="nw", text="Clued", fill="#F4F4F4", font=("Sedan Regular", 52))

        # Create the "AI" text
        clued_bbox = self.canvas.bbox(clued_text)
        clued_width = clued_bbox[2] - clued_bbox[0]
        self.canvas.create_text(415.0 + clued_width, 69.0, anchor="nw", text="AI", fill="#D71E1E", font=("Sedan Regular", 52))

        self.canvas.create_image(512.0, 277.0, image=self.image_refs["banner"])
        self.canvas.create_image(515.0, 397.56201171875, image=self.image_refs["divider"])

        self.entry_name = self.create_entry_with_icon(152.0, 420.0, 278.0, 51.0, "Name", "entry_bg_1", "entry_1", "icon")
        self.entry_age = self.create_entry_with_icon(152.0, 486.0, 278.0, 51.0, "Age", "entry_bg_1", "entry_1", "icon")
        self.entry_gender = self.create_entry_with_icon(152.0, 551.0, 278.0, 51.0, "Gender", "entry_bg_1", "entry_1", "icon")
        self.entry_appearance = self.create_entry_with_icon(629.0, 421.0, 281.0, 181.0, "Appearance", "entry_bg_2", "entry_2", "icon")

        submit_button = Button(image=self.image_refs["submit_button"], highlightthickness=0, command=self.submit_character, relief="flat")
        submit_button.place(x=338.0, y=642.0, width=355.0, height=53.0)

    def create_entry_with_icon(self, x, y, width, height, placeholder, bg_image_key, entry_image_key, icon_key):
        # Create background image
        self.canvas.create_image(x + 120, y + height / 2, image=self.image_refs[bg_image_key])
        
        # Create entry box image
        self.canvas.create_image(x + 139, y + height / 2, image=self.image_refs[entry_image_key])

        # Create entry widget
        entry = Entry(bd=0, bg="#292929", fg="#FFFFFF", font=("Inter", 13), highlightthickness=0)
        entry.insert(0, placeholder)
        entry.bind(self.focus, self.clear_default)
        entry.bind("<Return>", lambda event: self.submit_character())
        entry.place(x=x, y=y, width=width, height=height)

        # Create placeholder text
        self.canvas.create_text(x + 6, y + height / 2, anchor="nw", text=placeholder, fill="#FFFFFF", font=("Inter", 13))

        # Create icon images
        self.canvas.create_image(124.0,446.0,image=self.image_refs[icon_key])
        self.canvas.create_image(124.0,512.0,image=self.image_refs[icon_key])
        self.canvas.create_image(124.0,577.0,image=self.image_refs[icon_key])
        self.canvas.create_image(601.0,513.0,image=self.image_refs[icon_key])

        return entry  # Return the entry widget

    def clear_default(self, event):
        event.widget.delete(0, 'end')
        event.widget.unbind(self.focus)

    def submit_character(self):
        data = {
            "Name": self.entry_name.get(),
            "Age": self.entry_age.get(),
            "Gender": self.entry_gender.get(),
            "Appearance": self.entry_appearance.get()
        }

        if not all(data.values()):
            messagebox.showerror(title='Error', message='All fields must be completed.')
        else:
            insert_character(self.username, data)
            self.switch_to_chat(0, None, None)

    def clear(self):
        self.canvas.delete("all")
        self.image_refs = {}

    def hide(self):
        self.canvas.pack_forget()  # Hide canvas

    def get_window(self):
        return self.window
