import enum

class PlayState(enum.Enum):
    """
    Class representing the states for when a game is underway.
    """
    PLAYER_A_CHOOSING = 1
    PLAYER_B_CHOOSING = 2
    OTHER = 3
    END = 4