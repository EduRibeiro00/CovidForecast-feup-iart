from copy import deepcopy
from state import State

def move_left(state):
    """
    Moves the blank space to the left. Returns a new state.
    """
    board = deepcopy(state.get_board())
    x, y = state.get_blank_spot_coords()
    if y == 0: # if blank spot is already in the leftmost column
        return None

    board[x][y] = board[x][y - 1]
    board[x][y - 1] = 0
    return State(board)


def move_right(state):
    """
    Moves the blank space to the right. Returns a new state.
    """
    board = deepcopy(state.get_board())
    x, y = state.get_blank_spot_coords()
    board_size = state.get_board_size()
    if y == (board_size - 1):  # if blank spot is already in the rightmost column
        return None

    board[x][y] = board[x][y + 1]
    board[x][y + 1] = 0
    return State(board)


def move_down(state):
    """
    Moves the blank space down. Returns a new state.
    """
    board = deepcopy(state.get_board())
    x, y = state.get_blank_spot_coords()
    board_size = state.get_board_size()
    if x == (board_size - 1):  # if blank spot is already in the lowest row
        return None

    board[x][y] = board[x + 1][y]
    board[x + 1][y] = 0
    return State(board)


def move_up(state):
    """
    Moves the blank space up. Returns a new state
    """
    board = deepcopy(state.get_board())
    x, y = state.get_blank_spot_coords()
    if x == 0:  # if blank spot is already in the highest row
        return None

    board[x][y] = board[x - 1][y]
    board[x - 1][y] = 0
    return State(board)


operators = [
    move_left,
    move_right,
    move_up,
    move_down
]