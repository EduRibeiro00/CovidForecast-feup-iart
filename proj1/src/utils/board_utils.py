# constants for board chars
PLAYER_A_SOLDIER_CHAR = 'W'
PLAYER_B_SOLDIER_CHAR = 'B'
BLANK_SPACE_CHAR = ' '
NEUTRON_CHAR = 'N'

PLAYER_A = 'A'
PLAYER_B = 'B'
from copy import deepcopy



def create_initial_board(size):
    """
    Function that creates and returns the initial Neutron board with the referred size.
    """
    if (size % 2 == 0) or size > 11 or size < 5:
        raise ValueError("Invalid value for board size")

    board = []
    empty_rows = (size - 3) // 2

    # black line
    board.append([PLAYER_B_SOLDIER_CHAR] * size)

    for i in range(empty_rows):
        # blank line
        board.append([BLANK_SPACE_CHAR] * size)

    # create and append middle row with neutron
    middle_tile = size // 2
    middle_row = [BLANK_SPACE_CHAR] * size
    middle_row[middle_tile] = NEUTRON_CHAR
    board.append(middle_row)

    for i in range(empty_rows):
        # blank line
        board.append([BLANK_SPACE_CHAR] * size)

    # white line
    board.append([PLAYER_A_SOLDIER_CHAR] * size)

    return board

def determine_moves_neutron_soldier(current_board, minimax_board, size):
    """
       Function that determines and returns the the moves of the player (neutron move and soldier move)
    """
    found_old_neutron, found_new_neutron, found_old_soldier, found_new_soldier = False, False, False, False

    for i in range(size):
        for j in range(size):

            if current_board[i][j] == NEUTRON_CHAR:
                old_neutron = (i, j)
                found_old_neutron = True
            if minimax_board[i][j] == NEUTRON_CHAR:
                new_neutron = (i, j)
                found_new_neutron = True

            if minimax_board[i][j] != current_board[i][j]:
                if current_board[i][j] == BLANK_SPACE_CHAR and minimax_board[i][j] != NEUTRON_CHAR:
                    found_new_soldier = True
                    new_soldier = (i, j)
                elif current_board[i][j] == NEUTRON_CHAR and minimax_board[i][j] != BLANK_SPACE_CHAR:
                    found_new_soldier = True
                    new_soldier = (i, j)
                elif minimax_board[i][j] == BLANK_SPACE_CHAR and current_board[i][j] != NEUTRON_CHAR:
                    found_old_soldier = True
                    old_soldier = (i, j)

            if found_old_neutron and found_new_neutron and found_new_soldier and found_old_soldier:
                break

        if found_old_neutron and found_new_neutron and found_new_soldier and found_old_soldier:
            break

    if not found_old_soldier and not found_new_soldier:
        return ((old_neutron, new_neutron), None)

    return ((old_neutron, new_neutron), (old_soldier, new_soldier))