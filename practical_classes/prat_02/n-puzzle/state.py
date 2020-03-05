class State:
    """
    Class representing the state.
    """
    def __init__(self, board):
        """
        Constructor of the state.
        """
        self.board = board
        self.board_size = len(board)
        self.parent = None
        self.depth = 0

    def get_board(self):
        return self.board

    def get_board_size(self):
        return self.board_size

    def set_parent(self, state):
        self.parent = state
        self.depth = state.depth + 1


    def get_blank_spot_coords(self):
        for i in range(len(self.board)): # line index
            row = self.board[i]
            try:
                j = row.index(0) # column index
                return i, j
            except ValueError:
                continue

        return None


    def is_final_state(self):
        """
        Check if the state is final.
        :return: True or False
        """
        expected_value = 1

        for row in self.board:
            for cell in row:
                if expected_value == (self.board_size * self.board_size):
                    expected_value = 0

                if cell != expected_value:
                    return False

                expected_value += 1

        return True


    def get_g(self):
        """
        g function (number of plays to get to that board)
        """
        return self.depth


    def get_h(self):
        """
        h (heuristic) function (manhattan distances between the values and their supposed places)
        """
        sum = 0

        for i in range(self.board_size):
            for j in range(self.board_size):
                value = self.board[i][j]

                expected_row = (value - 1) / self.board_size
                expected_col = (value - 1) % self.board_size

                sum += (abs(expected_row - i) + abs(expected_col - j))

        return sum

    def print_state(self):
        print('---------')
        self.print_board()
        print('Depth: {depth}'.format(depth=self.depth))
        print('---------')

    def print_board(self):
        for row in self.board:
            print(*row)

    def __eq__(self, other):
        return self.board == other.board




def get_a_star_value(state):
    return state.get_g() + state.get_h()

def get_greedy_value(state):
    return state.get_h()

def get_uniform_cost_value(state):
    return state.get_g()