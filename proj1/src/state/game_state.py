import enum

class GameState(enum.Enum):
    """
    Class representing the main game states of the program.
    """
    MAIN_MENU = 1
    CHOOSE_BOARD_SIZE = 2
    MODE_SELECT = 3
    CHOOSE_DIFFICULTY = 4
    INSTRUCTIONS = 5
    PLAY_PREP = 6
    PLAY = 7
    GAME_OVER = 8
    EXIT = 9