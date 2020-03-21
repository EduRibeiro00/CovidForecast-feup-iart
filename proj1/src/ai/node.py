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


    def is_final_state(self, current_player):
        """
        Determines whether the state is final.
        """


    def get_neutron_piece(self):
        """
        Method that returns the coordinates of the neutron on the board.
        """
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == NEUTRON_CHAR:
                    return j, i


    def does_player_a_win(self, neutron_square_y):
        """
        Method that checks if player A has won.
        """
        if neutron_square_y == self.board_size - 1:
            return True
        return False


    def does_player_b_win(self, neutron_square_y):
        """
        Method that checks if player B has won.
        """
        if neutron_square_y == 0:
            return True
        return False


    def check_game_end(self):
        """
        Method that checks if the game has ended, and if so what was the result.
        """
        neutron_square_x, neutron_square_y = self.get_neutron_piece()
        if self.does_player_a_win(neutron_square_y):
            return True , PlayState.PLAYER_A_WINS

        elif self.does_player_b_win(neutron_square_y):
            return True, PlayState.PLAYER_B_WINS

        else:
            possible_moves_neutron = self.possible_moves(neutron_square_x, neutron_square_y)
            if len(possible_moves_neutron) == 0:
                if self.play_state == PlayState.PLAYER_A_MOVING_SOLDIER:
                    return True, PlayState.PLAYER_A_WINS
                elif self.play_state == PlayState.PLAYER_B_MOVING_SOLDIER:
                    return True, PlayState.PLAYER_B_WINS

        return False, None



    def draw_node_in_terminal(self):
        for row in self.board:
            print(*row)

