

class Node:
    """
    Class used to represent each board state/node.
    """
    def __init__(self, board, board_size):
        """
        Constructor of the class.
        """
        self.board = board
        self.board_size = board_size
        self.parent = None


    def set_parent(self, parent):
        """
        Function to set the parent of the state.
        """
        self.parent = parent


    def is_final_state(self, current_player):
        """
        Determines whether the state is final.
        """
        pass


    def draw_node_in_terminal(self):
        for row in self.board:
            print(*row)