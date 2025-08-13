import os
import sys
import ctypes
from ctypes import wintypes
import tkinter as tk
from ducktop.constants import Colours, Restrictions

# ----- Startup -----
    
def initialise_application(root, stay_on_top: bool = False):
    # Window settings
    root.overrideredirect(True)
    root.wm_attributes("-transparentcolor", Colours.TRANSPARENT) # choose a bg colour for transparency
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

def name_duck(root, duck):
    def set_name(event=None):
        duck.name = name_var.get()
        name_window.destroy()

    name_window = tk.Toplevel(root)
    name_window.overrideredirect(True)
    name_window.wm_attributes("-topmost", True)
    name_window.wm_attributes("-transparentcolor", Colours.TRANSPARENT)
    name_window.configure(bg=Colours.TRANSPARENT)

    canvas = tk.Canvas(
        name_window,
        width=160,
        height=40,
        bg=Colours.TRANSPARENT,
        highlightthickness=0,
        bd=0
    )
    canvas.pack()

    # Draw thicker rounded border
    def draw_rounded_box(x1, y1, x2, y2, r=10, **kwargs):
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)
    
    def on_type(event):
        current_text = entry.get()
        if len(current_text) > Restrictions.MAX_NAME_LENGTH:
            entry.delete(Restrictions.MAX_NAME_LENGTH, tk.END)

    draw_rounded_box(
        5, 5, 155, 35,
        r=12,
        fill="#F5F5F5",
        outline="#505050",
        width=2  # <-- Thicker border here
    )

    name_var = tk.StringVar()
    entry = tk.Entry(
        name_window,
        textvariable=name_var,
        font=('Arial', 10),
        fg='black',
        bg='#F5F5F5',
        relief='flat',
        border=0,
        insertbackground='black'
    )
    canvas.create_window(80, 20, window=entry, anchor='center')

    entry.bind("<KeyRelease>", on_type)
    entry.bind("<Return>", set_name)
    entry.focus_set()

    def update_position():
        name_window.geometry(f"+{duck.x}+{duck.y - 20}")
        name_window.after(10, update_position)

    update_position()

def open_settings_drop_down(root, duck):
    settings_menu = tk.Menu(root, tearoff=0, background='white')
    if duck.name != '':
        set_name = "Set Name"
        settings_menu.add_command(label=duck.name, compound='left', font=('Arial', 11, 'bold'), activebackground='white', activeforeground='black', foreground='black')
    else:
        set_name = "Rename"
    settings_menu.add_command(label=set_name, font=('Arial', 10), command=lambda: name_duck(root, duck))
    if duck.state.pet_state == 'sleeping':
        settings_menu.add_command(label="Wake Up", font=('Arial', 10), command=lambda: duck.wake_up())
    if duck.state.pet_state not in ['sleeping', 'sleep_from_standing', 'sleep_from_sitting', 'panic']:
        settings_menu.add_command(label="Sleep", font=('Arial', 10), command=lambda: duck.sleep())
    settings_menu.add_command(label="Reset", font=('Arial', 10), command=lambda: duck.state.set_state('idle'))
    settings_menu.add_command(label="Exit", font=('Arial', 10), command=root.quit)
    settings_menu.post(root.winfo_pointerx(), root.winfo_pointery())

def draw_speech_bubble(canvas, width, height, r=12, **kwargs):
    padding = 4
    tail_height = 8

    # Rounded box
    box = canvas.create_polygon(
        [
            padding + r, padding,
            width - padding - r, padding,
            width - padding, padding,
            width - padding, padding + r,
            width - padding, height - r,
            width - padding, height,
            width - padding - r, height,
            padding + r, height,
            padding, height,
            padding, height - r,
            padding, padding + r,
            padding, padding
        ],
        smooth=True,
        **kwargs
    )

    # Tail triangle pointing down
    triangle = canvas.create_polygon(
        [
            width // 2 - 6, height,
            width // 2 + 6, height,
            width // 2, height + tail_height
        ],
        fill=kwargs.get('fill', 'white'),
        outline=kwargs.get('outline', 'black'),
        width=kwargs.get('width', 1)
    )

    return box, triangle
