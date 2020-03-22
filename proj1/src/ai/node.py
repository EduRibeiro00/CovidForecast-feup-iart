from .operators import *
from utils.board_utils import *

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
        Determines whether the state is final at the start of a turn
        """
        neutron_x, neutron_y = self.get_neutron_coordinates()

        if neutron_y == 0:
            return True, PLAYER_A
        elif neutron_y == self.board_size - 1:
            return True, PLAYER_B
        else:
            moves_neutron = check_neutron_possible_moves(self, neutron_x, neutron_y)
            if current_player == PLAYER_A:
                if not moves_neutron:
                    return True, PLAYER_B
            elif current_player == PLAYER_B:
                if not moves_neutron:
                    return True, PLAYER_A

        return False, None

    def get_neutron_coordinates(self):
        """
        Method that returns the coordinates of the neutron on the board.
        """
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == NEUTRON_CHAR:
                    return j, i


    def check_neutron_possible_moves(self, neutron_x, neutron_y):

        for op in operators:
            if op(self, neutron_x, neutron_y) != None:
                return True
        return False


    # CHECK INDEX ORDER MAYBE SWITCHING THE J AND THE I

    def get_all_possible_nodes_for_player(self, current_player, neutron_turn):

        possible_nodes = []
        if neutron_turn:
            neutron_x, neutron_y = self.get_neutron_coordinates()
            possible_nodes = get_possible_nodes_for_piece(neutron_x, neutron_y)
            return possible_nodes

        else:
            for i in range(self.size):
                for j in range(self.size):
                    if current_player == PLAYER_A and self.board[i][j] == PLAYER_A_SOLDIER_CHAR:
                        possible_nodes_for_soldier = self.get_all_possible_nodes_for_player(j, i)
                        possible_nodes = possible_nodes + possible_nodes_for_soldier

                    elif current_player == PLAYER_B and self.board[i][j] == PLAYER_B_SOLDIER_CHAR:
                        possible_nodes_for_soldier = self.get_all_possible_nodes_for_player(j, i)
                        possible_nodes = possible_nodes + possible_nodes_for_soldier

    def get_possible_nodes_for_piece(self, piece_x, piece_y):

        possible_nodes = []

        for op in operators:
            new_node = op(self, piece_x, piece_y)
            if new_node != None:
                possible_nodes.append(new_node)

        return possible_nodes


    def draw_node_in_terminal(self):
        for row in self.board:
            print(*row)

