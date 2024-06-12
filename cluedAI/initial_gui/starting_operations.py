



from pathlib import Path
from tkinter import Canvas, PhotoImage, Tk

global ASSETS_PATH 

def create_window(directory):
    global ASSETS_PATH 
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(directory)
    
    window = Tk()
    window.geometry("1024x768")

    canvas = Canvas(
        window,
        bg = "#000000",
        height = 768,
        width = 1024,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)

    return window, canvas

def relative_to_assets(path: str) -> Path:
    global ASSETS_PATH 
    return ASSETS_PATH / Path(path)
