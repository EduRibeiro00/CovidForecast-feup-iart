from copy import deepcopy

# player 1 -> "O"
# player 2 -> "X"
class State:
    def __init__(self, board, num_moves=0):
        self.board = board
        self.parent = None
        self.depth = 0
        self.num_moves = num_moves

    def get_board(self):
        return self.board


    def set_parent(self, state):
        self.parent = state
        self.depth = state.depth + 1

    def is_final_state(self):
        """
        Tests if the game has ended, returning the char of the winner
        or returning an empty string if it was a draw.
        """
        if self.n_lines_4('X') > 0: return True, 'X'
        if self.n_lines_4('O') > 0: return True, 'O'
        if self.num_moves == 42: return True, ''

        return False, ''

    def n_lines_4(self, player):
        """
        Checks how many lines of four that player has on the board.
        """
        cnt = 0

        # check horizontal spaces
        for col in range(4):
            for row in range(6):
                if self.board[row][col] == player and self.board[row][col + 1] == player and self.board[row][col + 2] == player and self.board[row][col + 3] == player:
                    cnt += 1

        # check vertical spaces
        for col in range(7):
            for row in range(3):
                if self.board[row][col] == player and self.board[row + 1][col] == player and self.board[row + 2][col] == player and self.board[row + 3][col] == player:
                    cnt += 1

        # check / diagonal spaces
        for col in range(4):
            for row in range(3):
                if self.board[row][col] == player and self.board[row + 1][col + 1] == player and self.board[row + 2][col + 2] == player and self.board[row + 3][col + 3] == player:
                    cnt += 1

        # check \ diagonal spaces
        for col in range(4):
            for row in range(3, 6):
                if self.board[row][col] == player and self.board[row - 1][col + 1] == player and self.board[row - 2][col + 2] == player and self.board[row - 3][col + 3] == player:
                    cnt += 1

        return cnt


    def n_lines_3(self, player):
        """
        Checks how many lines of three (and blank space) that player has on the board.
        """
        cnt = 0

        # check horizontal spaces
        for col in range(4):
            for row in range(6):
                player_pieces = int((self.board[row][col] == player) + (self.board[row][col + 1] == player) + (self.board[row][col + 2] == player) + (self.board[row][col + 3] == player))
                empty_slots = int((self.board[row][col] == ' ') + (self.board[row][col + 1] == ' ') + (self.board[row][col + 2] == ' ') + (self.board[row][col + 3] == ' '))
                if player_pieces == 3 and empty_slots == 1:
                    cnt += 1

        # check vertical spaces
        for col in range(7):
            for row in range(3):
                player_pieces = int((self.board[row][col] == player) + (self.board[row + 1][col] == player) + (self.board[row + 2][col] == player) + (self.board[row + 3][col] == player))
                empty_slots = int((self.board[row][col] == ' ') + (self.board[row + 1][col] == ' ') + (self.board[row + 2][col] == ' ') + (self.board[row + 3][col] == ' '))
                if player_pieces == 3 and empty_slots == 1:
                    cnt += 1

        # check / diagonal spaces
        for col in range(4):
            for row in range(3):
                player_pieces = int((self.board[row][col] == player) + (self.board[row + 1][col + 1] == player) + (self.board[row + 2][col + 2] == player) + (self.board[row + 3][col + 3] == player))
                empty_slots = int((self.board[row][col] == ' ') + (self.board[row + 1][col + 1] == ' ') + (self.board[row + 2][col + 2] == ' ') + (self.board[row + 3][col + 3] == ' '))
                if player_pieces == 3 and empty_slots == 1:
                    cnt += 1

        # check \ diagonal spaces
        for col in range(4):
            for row in range(3, 6):
                player_pieces = int((self.board[row][col] == player) + (self.board[row - 1][col + 1] == player) + (self.board[row - 2][col + 2] == player) + (self.board[row - 3][col + 3] == player))
                empty_slots = int((self.board[row][col] == ' ') + (self.board[row - 1][col + 1] == ' ') + (self.board[row - 2][col + 2] == ' ') + (self.board[row - 3][col + 3] == ' '))
                if player_pieces == 3 and empty_slots == 1:
                    cnt += 1

        return cnt


    def central(self, player_char):
        value = 0

        for line in range(6):
            if self.board[line][3] == player_char:
                value += 1

            if self.board[line][5] == player_char:
                value += 1

            if self.board[line][4] == player_char:
                value += 2

        return value


    def get_score(self, player_char):
        if player_char == 'X':
            opp_char = 'O'
        else:
            opp_char = 'X'

        fav1 = self.n_lines_4(player_char) - self.n_lines_4(opp_char)
        fav2 = 100 * fav1 + self.n_lines_3(player_char) - self.n_lines_3(opp_char)
        fav3 = 100 * fav1 + self.central(player_char) - self.central(opp_char)
        fav4 = 5 * fav2 + fav3
        return fav4


    def get_possible_moves_for_player(self, player_char):
        """
        Get all possible moves for that player.
        """
        states = []
        for col_num in range(7):
            state = self.get_move_for_column(player_char, col_num)
            if state is not None:
                states.append((state, col_num))

        return states


    def get_move_for_column(self, player_char, col_num):
        """
        Returns the state that is generated if the current player
        plays on the specified column. Returns None if that
        column is already full
        """
        new_board = deepcopy(self.board)
        cur_line = 5 # starts in last line

        while cur_line >= 0:
            if new_board[cur_line][col_num] == ' ': # if slot is empty
                new_board[cur_line][col_num] = player_char
                return State(new_board, self.num_moves + 1)

            cur_line -= 1 # if not, skip to next line

        return None # column is totally full


    def print_state(self):
        """
        Prints the state on the board.
        """
        print('--------------------')
        for row in self.board:
            print(" ".join(row))
        print('--------------------')