from ai.state import Node
from utils.board_utils import create_initial_board
from interface.game_interface import GameInterface

class Game:
    """
    Main class representing the game.
    """
    def __init__(self, size):
        """
        Constructor of the class.
        """
        self.current_player = 'white' # white player starts first
        self.current_state = Node(create_initial_board(size), size) # create board with the wanted size
        self.interface = GameInterface(size)


    def run(self):
        """
        Main method of the game class. Contains the main game cycle.
        """
        self.interface.draw_background()


    def exit(self):
        """
        Method to exit.
        """
        self.interface.exit()