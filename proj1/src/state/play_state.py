import enum

class PlayState(enum.Enum):
    """
    Class representing the states for when a game is underway.
    """
    player_a_choosing = 1
    player_b_choosing = 2
    other = 3