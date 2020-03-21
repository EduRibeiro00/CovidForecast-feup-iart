from operators import *

WHITE_PLAYER = 'W'
BLACK_PLAYER = 'B'

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
        self.depth = 0


    def get_board(self):
        """
        Method that returns the current board.
        """
        return self.board


    def set_parent(self, parent):
        """
        Function to set the parent of the state.
        """
        self.parent = parent
        self.depth = self.parent.depth + 1

    def is_final_state(self, current_player):
        """
        Determines whether the state is final.
        """
        neutron_x, neutron_y = get_neutron_coordinates(self)
        if current_player == WHITE_PLAYER:
            return does_white_player_win(neutron_y)
        elif current_player == BLACK_PLAYER:
            return  does_black_player_win(neutron_y)

    def get_neutron_coordinates(self):
        """
        Method that returns the coordinates of the neutron on the board.
        """
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == NEUTRON_CHAR:
                    return j, i

    def does_white_player_win(self, neutron_x, neutron_y):
        """
        Method that checks if player A has won.
        """
        if neutron_square_y == self.board_size - 1:
            return True
        return not check_neutron_possible_moves(self, neutron_x, neutron_y)

    def does_black_player_win(self, neutron_x, neutron_y):
        """
        Method that checks if player B has won.
        """
        if neutron_square_y == 0:
            return True
        return not check_neutron_possible_moves(self, neutron_x, neutron_y)

    def check_neutron_possible_moves(self, neutron_x, neutron_y):

        for op in operators:
            if op(self, neutron_x, neutron_y) != None:
                return True
        return False



    def draw_node_in_terminal(self):
        for row in self.board:
            print(*row)

