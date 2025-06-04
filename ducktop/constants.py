

class Colours:
    TRANSPARENT = '#FF00FF'



class Probability:
    
    # When standing
    NO_ACTION_STANDING = 0.995
    TURN = 0.45
    WALK = 0.33
    SIT = 0.17
    SLEEP_STANDING = 0.05
    
    # When sitting
    NO_ACTION_SITTING= 0.999
    LOOK_AROUND = 0.8
    STAND_UP = 0.2
    SLEEP_SITTING = 0.1