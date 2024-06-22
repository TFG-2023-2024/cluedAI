from tkinter import Button, PhotoImage
from initial_gui.starting_operations import create_window, relative_to_assets

class StartScreen:
    def __init__(self, root, switch_to_login):
        """
        Initialize the StartScreen instance.

        This method sets up the initial state of the StartScreen, including
        creating a window with a canvas and loading necessary images.

        Args:
        - root (Tk): The root Tkinter window where the StartScreen will be displayed.
        - switch_to_login (function): Callback function to switch to the login screen.

        Attributes:
        - root (Tk): Reference to the root Tkinter window.
        - switch_to_login (function): Callback function to switch to the login screen.
        - window (Tk): Tkinter window instance created by create_window.
        - canvas (Canvas): Canvas widget within the window where elements are drawn.
        - image_refs (list): List to hold references to loaded images to prevent garbage collection.
        """
        self.root = root
        self.switch_to_login = switch_to_login
        self.window, self.canvas = create_window("assets/start", existing_root=root)
        self.image_refs = []  # List to hold references to images

    def show(self):
        """
        Show the StartScreen with its elements.

        This method loads images onto the canvas and creates UI elements such as
        buttons and text to display the start screen interface.
        """
        # Load images and keep references
        image_bg = PhotoImage(file=relative_to_assets("bg.png"))
        button_image_1 = PhotoImage(file=relative_to_assets("start_button.png"))

        # Store images in a list to prevent garbage collection
        self.image_refs.extend([image_bg, button_image_1])

        self.canvas.create_image(
            512.0,
            349.0,
            image=image_bg
        )

        button_1 = Button(
            image=button_image_1,
            highlightthickness=1,
            command=self.open_login,
            relief="flat"
        )
        button_1.place(
            x=334.0,
            y=667.0,
            width=355.0,
            height=53.0
        )

        clued_text = self.canvas.create_text(
            288.5,  # Center horizontally
            325.0,
            anchor="nw",
            text="clued",
            fill="#FFFFFF",
            font=("Inter SemiBold", 140 * -1)
        )

        clued_bbox = self.canvas.bbox(clued_text)
        clued_width = clued_bbox[2] - clued_bbox[0]

        self.canvas.create_text(
            288.5 + clued_width,
            325.0,
            anchor="nw",
            text="AI",
            fill="#D71E1E",
            font=("Inter Bold", 140 * -1)
        )

        self.canvas.create_text(
            267.0,
            483.0,
            anchor="nw",
            text="Embark on an enthralling journey through CluedAI, a murder" +
            "\nmystery interactive visual novel powered by generative AI. Delve" +
            "\ninto a meticulously crafted narrative where every decision shapes" +
            "\nthe investigation's outcome. Uncover clues, interrogate suspects," +
            "\nand navigate through twists and turns as you strive to solve the crime.",
            fill="#FFFFFF",
            font=("Inter", 18 * -1)
        )

    def open_login(self):
        """
        Switch to the login screen.

        This method calls the switch_to_login callback function to transition
        from the start screen to the login screen.
        """
        self.switch_to_login()

    def hide(self):
        """
        Hide the StartScreen canvas.

        This method hides the StartScreen canvas by packing it away.
        """
        self.canvas.pack_forget()