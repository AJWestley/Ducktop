from functools import partial
import tkinter as tk
import tkinter.font as tfont
from ducktop.pet import Duck
from ducktop.user_actions import start_drag, do_drag, stop_drag
from ducktop.utils import initialise_application, get_starting_position, clip_position, get_screen_height, open_settings_drop_down
from ducktop.rendering import NameBox
from ducktop.constants import Colours


def main():
    
    # ----- Application Startup -----
    root = tk.Tk()
    initialise_application(root, stay_on_top=True)

    screen_height = get_screen_height()
    screen_width = root.winfo_screenwidth()

    # ----- Create Duck -----
    x, y = get_starting_position(root)
    duck = Duck('idle', x, y, screen_width, screen_height)
    
    # ----- Recurring Functions -----
    def render_scene():

        duck.animator.next_frame()
        
        label.config(image=duck.animator.current_image)

        root.after(300, render_scene)

    def update_scene():
        
        duck.fall(screen_height)
        duck.update_state()
        clip_position(duck, screen_width, screen_height)
        
        root.geometry(f'+{duck.x}+{duck.y}')
        
        root.after(10, update_scene)
    
    
    # ----- Create Label -----
    label = tk.Label(root, bg=Colours.TRANSPARENT)
    label.pack()

    name_box = NameBox(root, duck)
    
    label.bind("<Button-1>", partial(start_drag, root=root, duck=duck))
    label.bind("<B1-Motion>", partial(do_drag, root=root, duck=duck))
    label.bind("<ButtonRelease-1>", partial(stop_drag, duck=duck))
    label.bind("<Button-3>", lambda _: open_settings_drop_down(root, duck))
    label.bind("<Enter>", lambda event: name_box.show_hover_name(duck, event))
    label.bind("<Leave>", lambda event: name_box.hide_hover_name(event))
    name_box.hover_name_window.withdraw()
    
    
    # ----- Set Initial Position -----
    root.geometry(f"+{duck.x}+{duck.y}")
    
    # ----- Create Update Loop -----
    render_scene()
    update_scene()
    name_box.update_hover_position(duck, root)

    root.mainloop()

if __name__ == '__main__': main()