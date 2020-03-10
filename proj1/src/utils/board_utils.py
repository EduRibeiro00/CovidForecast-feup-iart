# constants for board chars
PLAYER_A_SOLDIER_CHAR = 'W'
PLAYER_B_SOLDIER_CHAR = 'B'
BLANK_SPACE_CHAR = ' '
NEUTRON_CHAR = 'N'


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