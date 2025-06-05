class Restrictions:
    MAX_NAME_LENGTH = 20

class Colours:
    TRANSPARENT = '#FF00FF'

class Probability:
    
    # When standing
    NO_ACTION_STANDING = 0.995
    TURN = 0.35
    WALK = 0.25
    SIT = 0.15
    SLEEP_STANDING = 0.05
    
    # When sitting
    NO_ACTION_SITTING= 0.999
    LOOK_AROUND = 0.7
    STAND_UP = 0.2
    SLEEP_SITTING = 0.1