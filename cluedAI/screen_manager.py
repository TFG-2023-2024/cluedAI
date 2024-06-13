import tkinter as tk
from initial_gui.reroll_screen import RerollScreen
from initial_gui.start_screen import StartScreen
from initial_gui.login_screen import LoginScreen
from initial_gui.create_screen import CreateScreen
from initial_gui.game_screen import ChatScreen
from initial_gui.select_screen import SelectScreen

class ScreenManager:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x768")  # Set the window size
        self.current_screen = None
        self.day = 0  # Example attribute, if needed
        
    def clear_screen(self):
        if self.current_screen:
            self.current_screen.hide()

    def update_focus(self):
        # Focus management
        self.root.focus_set()  # Set focus to the root window
        self.root.update_idletasks()  # Ensure all idle tasks (like focus updates) are handled
    
    def switch_to_start(self):
        self.clear_screen()
        self.current_screen = StartScreen(self.root, self.switch_to_login)
        self.current_screen.show()
        self.update_focus()
    
    def switch_to_login(self):
        self.clear_screen()
        self.current_screen = LoginScreen(self.root, self.switch_to_create)
        self.current_screen.show()
        self.update_focus()
    
    def switch_to_create(self, username):
        self.clear_screen()
        self.current_screen = CreateScreen(self.root, self.switch_to_chat, username)
        self.current_screen.show()
        self.update_focus()
    
    def switch_to_chat(self, reroll=None):
        self.clear_screen()
        if reroll:
            self.current_screen = ChatScreen(self.root, self.switch_to_select, self.switch_to_reroll, self.day, reroll)
        else:
            self.current_screen = ChatScreen(self.root, self.switch_to_select, self.switch_to_reroll, self.day)
        self.update_focus()
    
    def switch_to_select(self, day):
        self.clear_screen()
        self.current_screen = SelectScreen(self.root, self.switch_to_chat, day)
        self.update_focus()

    def switch_to_reroll(self, day, response):
        self.clear_screen()
        self.current_screen = RerollScreen(self.root, self.switch_to_chat, day, response)
        self.update_focus()

def main():
    root = tk.Tk()  # Create the Tk instance here
    root.geometry("1024x768")  # Set window size if needed

    manager = ScreenManager(root)
    manager.switch_to_chat()  # Start with the start screen

    root.mainloop()  # Start the main loop here

if __name__ == "__main__":
    main()
