import random
from ducktop.rendering import AnimationHandler, load_duck_animations
from ducktop.state_handler import State

P_REMAIN = 0.995
P_TURN = 0.5
P_WALK = 0.4

class Duck:
    def __init__(self, start_state, x, y, sw, sh):
    
        self.x = x
        self.y = y
        
        self.state = State(start_state, 'left')
        
        animations = load_duck_animations()
        
        self.animator = AnimationHandler(animations, 'blinking', self.state.facing, 32, 32)
        
        self.sw = sw
        self.sh = sh
    
    def update_state(self):
        if self.state.falling:
            self.y += 2
        
        if self.state.pet_state == 'walking':
            velocity = 1 if self.state.facing == 'right' else -1
            self.x += velocity
            
            if self.x - 5 < self.state.destination < self.x + 5:
                self.state.set_state('blinking')
        
        if self.state.pet_state == 'blinking' and not self.state.falling:
            if random.uniform(0, 1) > P_REMAIN:
                self.change_state()
        
        if self.state.pet_state == 'turn' and self.animator.frame >= self.animator.num_frames - 1:
            self.state.set_state('blinking')
        
        if self.state.pet_state == 'pecking_floor' and self.animator.frame >= self.animator.num_frames - 1:
            self.state.set_state('blinking')
            
        self.update_spritesheet()
    
    def update_spritesheet(self):
        self.animator.set_spritesheet(self.state.pet_state)
    
    def change_state(self):
        cumulative = P_TURN
        rand = random.uniform(0, 1)
        
        if rand < cumulative:
            self.turn_around()
            return
        
        cumulative += P_WALK
        
        if rand < cumulative:
            self.start_walking()
            return
        
        self.peck_ground()
    
    def turn_around(self):
        if self.state.facing == 'left':
            self.state.facing = 'right'
        else:
            self.state.facing = 'left'
        self.state.pet_state = 'turn'
        self.animator.set_direction(self.state.facing)
    
    def start_walking(self):
        if (self.state.facing == 'right' and self.x > 3 * self.sw / 4) or (self.state.facing == 'left' and self.x < self.sw / 4):
            self.turn_around()
            return
        
        if self.state.facing == 'right':
            self.state.destination = random.randint(self.x + 50, self.sw - 32)
        
        if self.state.facing == 'left':
            self.state.destination = random.randint(-32, self.x - 50)
        
        self.state.set_state('walking')
    
    def peck_ground(self):
        self.state.pet_state = 'pecking_floor'
    
    def fall(self, screen_height):
        if self.y < screen_height- 65 and not self.state.grabbed:
            self.state.set_falling(True)
        else:
            self.state.set_falling(False)
