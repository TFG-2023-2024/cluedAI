import os
import tkinter as tk
from initial_gui.reroll_screen import RerollScreen
from initial_gui.start_screen import StartScreen
from initial_gui.login_screen import LoginScreen
from initial_gui.create_screen import CreateScreen
from initial_gui.game_screen import ChatScreen
from initial_gui.select_screen import SelectScreen

class ScreenManager:
    def __init__(self, root):
        """
        Initialize the ScreenManager.

        Args:
        - root (tk.Tk): The Tkinter root window.
        """
        self.root = root
        self.root.geometry("1024x768")
        self.current_screen = None
        
    def clear_screen(self):
        """
        Clear the current screen by hiding it.

        This method hides the current screen if there is one displayed.
        """
        if self.current_screen:
            self.current_screen.hide()

    def update_focus(self):
        """
        Update the focus to the root window.

        This method sets the focus to the root window and updates all idle tasks.
        """
        self.root.focus_set()
        self.root.update_idletasks()
    
    def switch_to_start(self):
        """
        Switch to the start screen.

        This method clears the current screen, switches to the StartScreen,
        displays it, and updates the focus.
        """
        self.clear_screen()
        self.current_screen = StartScreen(self.root, self.switch_to_login)
        self.current_screen.show()
        self.update_focus()
    
    def switch_to_login(self):
        """
        Switch to the login screen.

        This method clears the current screen, switches to the LoginScreen,
        displays it, and updates the focus.
        """
        self.clear_screen()
        self.current_screen = LoginScreen(self.root, self.switch_to_create)
        self.current_screen.show()
        self.update_focus()
    
    def switch_to_create(self, username):
        """
        Switch to the create screen.

        This method clears the current screen, switches to the CreateScreen,
        displays it with the provided username, and updates the focus.

        Args:
        - username (str): The username to pass to the CreateScreen.
        """
        self.clear_screen()
        self.current_screen = CreateScreen(self.root, self.switch_to_chat, username)
        self.current_screen.show()
        self.update_focus()
    
    def switch_to_chat(self, day, id, type, reroll=None):
        """
        Switch to the chat screen.

        This method clears the current screen, switches to the ChatScreen,
        displays it with the provided parameters, including an optional reroll,
        and updates the focus.

        Args:
        - day (str): The day parameter for the ChatScreen.
        - id (str): The id parameter for the ChatScreen (Character or Item id).
        - type (str): The type parameter for the ChatScreen (Either Item or Character).
        - reroll (any): Optional parameter for reroll information.
        """
        self.clear_screen()
        if reroll:
            self.current_screen = ChatScreen(self.root, self.switch_to_select, self.switch_to_reroll, day, id, type, reroll)
        else:
            self.current_screen = ChatScreen(self.root, self.switch_to_select, self.switch_to_reroll, day, id, type, None)
        self.update_focus()

    
    def switch_to_select(self, day, data):
        """
        Switch to the select screen.

        This method clears the current screen, switches to the SelectScreen,
        displays it with the provided parameters, and updates the focus.

        Args:
        - day (str): The day parameter for the SelectScreen.
        - data (any): The data parameter for the SelectScreen includes locations selected.
        """
        self.clear_screen()
        self.current_screen = SelectScreen(self.root, self.switch_to_chat, day, data)
        self.update_focus()

    def switch_to_reroll(self, day, response, id):
        """
        Switch to the reroll screen.

        This method clears the current screen, switches to the RerollScreen,
        displays it with the provided parameters, and updates the focus.

        Args:
        - day (str): The day parameter for the RerollScreen.
        - response (any): The response to be rerolled.
        - id (str): The id parameter for the RerollScreen (Assistant id).
        """
        self.clear_screen()
        self.current_screen = RerollScreen(self.root, self.switch_to_chat, day, response, id)
        self.update_focus()

def basic_window():
    """
    Initialize and run the main Tkinter window for the application.

    This function creates a Tkinter root window, sets its size, title, and icon,
    initializes the ScreenManager to manage different screens of the application,
    switches to the start screen, and starts the main event loop.
    """
    root = tk.Tk()  
    root.geometry("1024x768") 
    root.title("cluedAI")

    ruta_actual = os.path.dirname(__file__)

    ruta_icono = os.path.join(ruta_actual, "initial_gui", "image.ico")
    root.iconbitmap(ruta_icono)
        
    manager = ScreenManager(root)
    manager.switch_to_start()

    root.mainloop() 


