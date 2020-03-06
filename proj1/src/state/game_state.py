import enum

class GameState(enum.Enum):
    """
    Class representing the main game states of the program.
    """
    MAIN_MENU = 1
    PLAYER_SELECT = 2
    DIFFICULTY = 3
    PLAY = 4
    EXIT = 5