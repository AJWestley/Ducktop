import os
import sys
import ctypes
from ctypes import wintypes

# ----- Constants -----

TRANSPARENT = '#FF00FF'


# ----- Startup -----
    
def initialise_application(root, stay_on_top: bool = False):
    # Window settings
    root.overrideredirect(True)
    root.wm_attributes("-transparentcolor", TRANSPARENT) # choose a bg colour for transparency
    if stay_on_top:
        root.wm_attributes("-topmost", True)

def get_starting_position(root):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    return 5 * screen_width // 6, screen_height // 2 # start in middle right


# ----- Auxilliary Methods -----
def clip_position(duck, screen_width, screen_height):
    if duck.y > screen_height - 65:
        duck.y = screen_height - 65
    
    if duck.x < -32:
        duck.x = -32
        
    if duck.x > screen_width - 32:
        duck.x = screen_width - 32

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS  # Temporary folder for PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_screen_height():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()

    # RECT is a structure that contains information about a rectangle (left, top, right, bottom)
    rect = wintypes.RECT()

    # SystemParametersInfoW with SPI_GETWORKAREA gives us the work area (screen area excluding taskbar)
    ctypes.windll.user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(rect), 0)

    # `rect.top` will give us the top coordinate of the taskbar
    taskbar_top = rect.bottom  # this is the y-position where the taskbar starts
    
    return taskbar_top