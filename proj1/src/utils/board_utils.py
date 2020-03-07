def create_initial_board(size):
    """
    Function that creates and returns the initial Neutron board with the referred size.
    """
    if (size % 2 == 0) or size > 11 or size < 5:
        raise ValueError("Invalid value for board size")

    board = []
    empty_rows = (size - 3) // 2

    white = 'W'
    black = 'B'
    neutron = 'N'
    blank = ' '

    # black line
    board.append([black] * size)

    for i in range(empty_rows):
        # blank line
        board.append([blank] * size)

    # create and append middle row with neutron
    middle_tile = size // 2
    middle_row = [blank] * size
    middle_row[middle_tile] = neutron
    board.append(middle_row)

    for i in range(empty_rows):
        # blank line
        board.append([blank] * size)

    # white line
    board.append([white] * size)

    return board