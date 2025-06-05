from PIL import Image, ImageTk
import tkinter as tk
import tkinter.font as tfont
from ducktop.utils import resource_path, draw_speech_bubble
from ducktop.constants import Colours

class AnimationHandler:
    def __init__(self, animation_map, starting_animation, starting_direction, frame_width, frame_height):
        self.animation_map = animation_map
        
        self.frame_width = frame_width
        self.frame_height = frame_height
        
        self.facing = starting_direction
        self.curr_animation = starting_animation
        
        self.frame = 0
        self.sprite_sheet = self.animation_map[starting_direction][starting_animation]['sprite_sheet']
        self.num_frames = self.animation_map[starting_direction][starting_animation]['num_frames']
        self.current_image = None
    
    def next_frame(self):
        # Crop the 32x32 region from the sprite sheet
        left = self.frame * self.frame_width
        upper = 0
        right = left + self.frame_width
        lower = upper + self.frame_height
        frame = self.sprite_sheet.crop((left, upper, right, lower)).convert('RGB')

        # Resize frame (optional)
        scale = 2
        frame = frame.resize((self.frame_width * scale, self.frame_height * scale), Image.Resampling.NEAREST)

        # Update image
        self.current_image = ImageTk.PhotoImage(frame)

        # Next frame
        self.frame = (self.frame + 1) % self.num_frames
    
    def set_spritesheet(self, new_animation):
        if new_animation == self.curr_animation:
            return
        self.sprite_sheet = self.animation_map[self.facing][new_animation]['sprite_sheet']
        self.num_frames = self.animation_map[self.facing][new_animation]['num_frames']
        self.curr_animation = new_animation
        self.frame = 0
    
    def set_direction(self, new_direction):
        self.facing = new_direction
        self.sprite_sheet = self.animation_map[self.facing][self.curr_animation]['sprite_sheet']
        self.frame = 0

class NameBox:
    def __init__(self, root, duck):
        self.font = tfont.Font(family='Arial', size=10, weight='bold')
        self.hover_name_window = tk.Toplevel(root)
        self.hover_name_window.overrideredirect(True)
        self.hover_name_window.wm_attributes("-topmost", True)
        self.hover_name_window.wm_attributes("-transparentcolor", Colours.TRANSPARENT)
        self.hover_name_window.configure(bg=Colours.TRANSPARENT)

        self.canvas = tk.Canvas(
            self.hover_name_window,
            width=160,
            height=40,
            bg=Colours.TRANSPARENT,
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack()
    
    def update_hover_position(self, duck, root):
        if self.hover_name_window.winfo_ismapped():
            x = duck.x
            y = duck.y - 20
            self.hover_name_window.geometry(f"+{x}+{y}")
        root.after(10, lambda: self.update_hover_position(duck, root))
    
    def show_hover_name(self, duck, event):
        if duck.name.strip() == "":
            return

        name_width = self.font.measure(duck.name)
        padding = 20
        bubble_width = name_width + padding
        bubble_height = 36
        tail_height = 8

        bubble_width = max(60, min(bubble_width, 300))
        total_height = bubble_height + tail_height

        self.canvas.config(width=bubble_width, height=total_height)
        self.canvas.delete("all")

        draw_speech_bubble(
            self.canvas,
            width=bubble_width,
            height=bubble_height,
            r=12,
            fill="#F5F5F5",
            outline="#505050"
        )

        self.canvas.create_text(
            bubble_width // 2, bubble_height // 2,
            text=duck.name,
            fill="black",
            font=self.font
        )

        x = duck.x
        y = duck.y - 20

        self.hover_name_window.geometry(f"+{x}+{y}")
        self.hover_name_window.deiconify()
    
    def hide_hover_name(self, event):
        self.hover_name_window.withdraw()

directions = ['left', 'right']
animation_types = {
    'idle',
    'flying',
    'jump',
    'panic',
    'pecking_floor',
    'sitting_idle',
    'sitting_down',
    'sitting_looking_around',
    'sleep_from_sitting',
    'sleep_from_standing',
    'sleeping',
    'stand_up',
    'turn',
    'waking_up',
    'walking'
}

def load_duck_animations(folder = 'ducktop/animations', frame_width = 32):
    animations = {}
    for direction in directions:
        animations[direction] = {}
        for ani_type in animation_types:
            path = resource_path(f"{folder}/{ani_type}_{direction}.png")
            sprite_sheet = Image.open(path)
            num_frames = sprite_sheet.width // frame_width
            animations[direction][ani_type] = {'sprite_sheet': sprite_sheet, 'num_frames': num_frames}
    return animations