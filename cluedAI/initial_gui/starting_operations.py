from pathlib import Path
from tkinter import Canvas, PhotoImage, Tk

global ASSETS_PATH

def create_window(directory, existing_root=None):
    """
    Create a new Tkinter window with a canvas.

    This function sets up a new Tkinter window with a canvas of specified dimensions
    and background color. It optionally uses an existing Tk instance if provided,
    otherwise, it creates a new one.

    Args:
    - directory (str): Directory name where assets are stored.
    - existing_root (Tk, optional): Existing Tk instance to use for the window.

    Returns:
    - window (Tk): Tkinter window instance.
    - canvas (Canvas): Canvas widget within the window.
    """
    global ASSETS_PATH
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(directory)

    if existing_root:
        window = existing_root
    else:
        window = Tk()
        window.geometry("1024x768")

    canvas = Canvas(
        window,
        bg="#000000",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)

    return window, canvas

def relative_to_assets(path: str) -> Path:
    """
    Return the absolute path of a file relative to the assets directory.

    This function takes a relative path to a file within the assets directory
    and returns its absolute path.

    Args:
    - path (str): Relative path of the file within the assets directory.

    Returns:
    - absolute_path (Path): Absolute path of the file within the assets directory.
    """
    global ASSETS_PATH
    return ASSETS_PATH / Path(path)
