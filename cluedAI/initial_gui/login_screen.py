from tkinter import Entry, Button, PhotoImage, messagebox
from initial_gui.starting_operations import create_window, relative_to_assets
from users.user_operations import log_user

class LoginScreen:
    def __init__(self, root, switch_to_create):
        self.root = root
        self.switch_to_create = switch_to_create
        self.window, self.canvas = create_window("assets/login", existing_root=root)
        self.focus = '<FocusIn>'
        self.username_text = "Enter your username"
        self.entry_key = None
        self.entry_username = None
        self.image_refs = {}

    def show(self):
        self.load_images()
        self.create_ui_elements()

    def load_images(self):
        self.image_refs["bg"] = PhotoImage(file=relative_to_assets("bg.png"))
        self.image_refs["login_button"] = PhotoImage(file=relative_to_assets("login_button.png"))
        self.image_refs["entry_bg"] = PhotoImage(file=relative_to_assets("entry_bg.png"))
        self.image_refs["entry"] = PhotoImage(file=relative_to_assets("entry.png"))
        self.image_refs["icon_1"] = PhotoImage(file=relative_to_assets("icon_1.png"))
        self.image_refs["entry_bg_2"] = PhotoImage(file=relative_to_assets("entry_bg.png"))
        self.image_refs["entry_2"] = PhotoImage(file=relative_to_assets("entry.png"))
        self.image_refs["icon_2"] = PhotoImage(file=relative_to_assets("icon_2.png"))
        self.image_refs["banner"] = PhotoImage(file=relative_to_assets("banner.png"))

    def create_ui_elements(self):
        self.canvas.create_image(515.0, 390.0, image=self.image_refs["bg"])

        login_button = Button(image=self.image_refs["login_button"], highlightthickness=0, command=self.create_character, relief="flat")
        login_button.place(x=334.0, y=634.0, width=355.0, height=53.0)

        self.canvas.create_image(511.0, 546.0, image=self.image_refs["entry_bg"])
        self.canvas.create_image(531.0, 546.0, image=self.image_refs["entry"])

        self.entry_key = Entry(bd=0, bg="#292929", fg="#FFFFFF", font=("Inter", 13), highlightthickness=0)
        self.entry_key.insert(0, "Enter your API Key")
        self.entry_key.bind(self.focus, self.clear_default)
        self.entry_key.bind("<Return>", lambda event: self.create_character())
        self.entry_key.place(x=393.0, y=521.0, width=276.0, height=51.0)

        self.canvas.create_image(365.0, 546.0, image=self.image_refs["icon_1"])

        self.canvas.create_image(511.0, 448.0, image=self.image_refs["entry_bg_2"])
        self.canvas.create_image(531.0, 448.0, image=self.image_refs["entry_2"])

        self.entry_username = Entry(bd=0, bg="#292929", fg="#FFFFFF", highlightthickness=0)
        self.entry_username.insert(0, self.username_text)
        self.entry_username.bind(self.focus, self.clear_default)
        self.entry_username.bind("<Return>", lambda event: self.create_character())
        self.entry_username.place(x=393.0, y=422.0, width=276.0, height=51.0)

        self.canvas.create_text(397.0, 440.0, anchor="nw", text=self.username_text, fill="#FFFFFF", font=("Inter", 13))

        self.canvas.create_image(363.0, 448.0, image=self.image_refs["icon_2"])

        self.canvas.create_text(418.0, 142.0, anchor="nw", text="Please Login To Your Account", fill="#7B7B7B", font=("Inter Light", 13))

        clued_text = self.canvas.create_text(415.0, 69.0, anchor="nw", text="Clued", fill="#F4F4F4", font=("Sedan Regular", 52))
        clued_bbox = self.canvas.bbox(clued_text)
        clued_width = clued_bbox[2] - clued_bbox[0]
        self.canvas.create_text(415.0 + clued_width, 69.0, anchor="nw", text="AI", fill="#D71E1E", font=("Sedan Regular", 52))

        self.canvas.create_image(512.0, 277.0, image=self.image_refs["banner"])

    def create_character(self):
        api = self.entry_key.get()
        username = self.entry_username.get()

        if not api or not username or api == "Enter your API Key" or username == self.username_text:
            messagebox.showerror(title='Error', message='Both fields must be completed.', icon="error")
        else:
            log_user(username)
            self.switch_to_create(username)

    def clear_default(self, event):
        event.widget.delete(0, 'end')
        event.widget.unbind(self.focus)

    def clear(self):
        self.canvas.delete("all")
        self.image_refs = {}

    def hide(self):
        self.canvas.pack_forget()  # Hide canvas

    def get_window(self):
        return self.window
