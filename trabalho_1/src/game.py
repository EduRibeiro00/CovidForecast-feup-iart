from state import State
from utils.board_utils import create_initial_board

class Game:
    """
    Main class representing the game.
    """
    def __init__(self, size):
        """
        Constructor of the class.
        """
        self.current_player = 'white' # white player starts first
        self.current_state = State(create_initial_board(size), size) # create board with the wanted size


    def run(self):
        """
        Main method of the game class. Contains the main game cycle.
        """
        self.current_state.draw_state()