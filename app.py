from functools import partial
import tkinter as tk
from pet import Duck
from user_actions import start_drag, do_drag, stop_drag
import utils

def render_scene():
    global duck

    duck.animator.next_frame()
    
    label.config(image=duck.animator.current_image)

    root.after(300, render_scene)

def update_scene():
    global duck
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    
    duck.fall(sh)
    duck.update_state()
    utils.clip_position(duck, sw, sh)
    
    root.geometry(f'+{duck.x}+{duck.y}')
    
    root.after(10, update_scene)

if __name__ == '__main__':
    
    # ----- Application Startup -----
    root = tk.Tk()
    utils.initialise_application(root, stay_on_top=True)


    # ----- Create Duck -----
    x, y = utils.get_starting_position(root)
    duck = Duck('blinking', x, y, root.winfo_screenmmwidth(), root.winfo_screenmmheight())
    
    
    # ----- Create Label -----
    label = tk.Label(root, bg=utils.TRANSPARENT)
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