from functools import partial
import tkinter as tk
from ducktop.pet import Duck
from ducktop.user_actions import start_drag, do_drag, stop_drag
from ducktop.utils import initialise_application, get_starting_position, clip_position, get_screen_height
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
    
    label.bind("<Button-1>", partial(start_drag, root=root, duck=duck))
    label.bind("<B1-Motion>", partial(do_drag, root=root, duck=duck))
    label.bind("<ButtonRelease-1>", partial(stop_drag, duck=duck))
    
    
    # ----- Set Initial Position -----
    root.geometry(f"+{duck.x}+{duck.y}")
    
    # ----- Create Update Loop -----
    render_scene()
    update_scene()

    root.mainloop()

if __name__ == '__main__': main()