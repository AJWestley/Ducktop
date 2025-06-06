import tkinter as tk
from ducktop.utils import clip_position, get_screen_height

def start_drag(event, *, root=None, duck=None):
    ''' Begins the action of dragging the pet around '''
    root._drag_start_x = event.x
    root._drag_start_y = event.y
    duck.state.set_grabbed(True)

def do_drag(event, *, root=None, duck=None):
    ''' Glues the pet to user's cursor '''
    duck.x = root.winfo_x() + (event.x - root._drag_start_x)
    duck.y = root.winfo_y() + (event.y - root._drag_start_y)
    clip_position(duck, root.winfo_screenwidth(), get_screen_height())
    root.geometry(f"+{duck.x}+{duck.y}")

def stop_drag(event, *, duck=None):
    ''' Ends the action of dragging the pet around '''
    duck.state.set_grabbed(False)