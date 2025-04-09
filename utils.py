import tkinter as tk

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
