import random
from ducktop.rendering import AnimationHandler, load_duck_animations
from ducktop.state_handler import State
from ducktop.constants import Probability

class Duck:
    def __init__(self, start_state, x, y, sw, sh):
    
        self.x = x
        self.y = y
        
        self.state = State(start_state, 'left')
        
        animations = load_duck_animations()
        
        self.animator = AnimationHandler(animations, 'idle', self.state.facing, 32, 32)
        
        self.sw = sw
        self.sh = sh
    
    def update_state(self):
        if self.state.falling:
            self.y += 2
        
        if self.state.pet_state == 'walking':
            velocity = 1 if self.state.facing == 'right' else -1
            self.x += velocity
            
            if self.x - 5 < self.state.destination < self.x + 5:
                self.state.set_state('idle')
        
        if self.state.pet_state == 'idle' and not self.state.falling:
            if random.uniform(0, 1) > Probability.NO_ACTION_STANDING:
                self.change_state()
        
        if self.state.pet_state == 'sitting_idle' and not self.state.falling:
            if random.uniform(0, 1) > Probability.NO_ACTION_SITTING:
                self.change_state()
        
        if self.state.pet_state == 'turn' and self.end_of_animation():
            self.state.set_state('idle')
        
        if self.state.pet_state == 'pecking_floor' and self.end_of_animation():
            self.state.set_state('idle')
        
        if self.state.pet_state == 'sitting_down' and self.end_of_animation():
            self.state.set_state('sitting_idle')
        
        if self.state.pet_state == 'stand_up' and self.end_of_animation():
            self.state.set_state('idle')
        
        if self.state.pet_state == 'sitting_looking_around' and self.end_of_animation():
            self.state.set_state('sitting_idle')
            
        self.update_spritesheet()
    
    def update_spritesheet(self):
        self.animator.set_spritesheet(self.state.pet_state)
    
    def change_state(self):
        rand = random.uniform(0, 1)
        
        if self.state.pet_state == 'idle':
            if rand < Probability.TURN:
                self.turn_around()
                return
            
            rand -= Probability.TURN
            
            if rand < Probability.WALK:
                self.start_walking()
                return
            
            rand -= Probability.WALK
            
            if rand < Probability.SIT:
                self.sit_down()
                return
            
            self.peck_ground()
        
        elif self.state.pet_state == 'sitting_idle':
            if rand < Probability.LOOK_AROUND:
                self.look_around_sitting()
                return
            
            rand -= Probability.LOOK_AROUND
            
            if rand < Probability.STAND_UP:
                self.stand_up()
                return
    
    def turn_around(self):
        if self.state.facing == 'left':
            self.state.facing = 'right'
        else:
            self.state.facing = 'left'
        self.state.pet_state = 'turn'
        self.animator.set_direction(self.state.facing)
        self.animator.frame = 0
    
    def start_walking(self):
        if (self.state.facing == 'right' and self.x > 3 * self.sw / 4) or (self.state.facing == 'left' and self.x < self.sw / 4):
            self.turn_around()
        
        elif self.state.facing == 'right':
            self.state.destination = random.randint(self.x + 50, self.sw - 32)
        
        elif self.state.facing == 'left':
            self.state.destination = random.randint(-32, self.x - 50)
        
        self.state.set_state('walking')
    
    def sit_down(self):
        self.state.set_state('sitting_down')
        self.animator.frame = 0
    
    def stand_up(self):
        self.state.set_state('stand_up')
        self.animator.frame = 0
    
    def peck_ground(self):
        self.state.pet_state = 'pecking_floor'
        self.animator.frame = 0
    
    def fall(self, screen_height):
        if self.y < screen_height- 65 and not self.state.grabbed:
            self.state.set_falling(True)
        else:
            self.state.set_falling(False)
    
    def look_around_sitting(self):
        self.state.set_state('sitting_looking_around')
        self.animator.frame = 0
    
    def end_of_animation(self):
        return self.animator.frame >= self.animator.num_frames - 1
