class State:
    def __init__(self, init_state, facing):
        self.pet_state = None
        self.set_state(init_state)
        self.facing = facing
        self.grabbed = False
        self.falling = False
        self.destination = 0
    
    def set_state(self, state):
        if self.pet_state == state:
            return
        self.pet_state = state

    def set_direction(self, dir):
        if dir == self.facing:
            return
        self.facing = dir
    
    def set_grabbed(self, grabbed):
        self.grabbed = grabbed
        if grabbed:
            self.set_state('panic')
    
    def set_falling(self, falling):
        self.falling = falling