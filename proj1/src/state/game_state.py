import enum

class GameState(enum.Enum):
    """
    Class representing the main game states of the program.
    """
    MAIN_MENU = 1
    CHOOSE_BOARD_SIZE = 2
    MODE_SELECT = 3
    CHOOSE_DIFFICULTY_A = 4
    CHOOSE_DIFFICULTY_B = 5
    INSTRUCTIONS = 6
    PLAY_PREP = 7
    PLAY = 8
    GAME_OVER = 9
    EXIT = 10