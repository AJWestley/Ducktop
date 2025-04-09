from PIL import Image, ImageTk
from ducktop.utils import resource_path

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


directions = ['left', 'right']
animation_types = {
    'blinking',
    'flying',
    'jump',
    'panic',
    'pecking_floor',
    'sitting_blinking',
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