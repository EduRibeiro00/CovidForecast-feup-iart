import enum

class GameState(enum.Enum):
    """
    Class representing the main game states of the program.
    """
    main_menu = 1
    player_select = 2
    difficulty = 3
    play = 4