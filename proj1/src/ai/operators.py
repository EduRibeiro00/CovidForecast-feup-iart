from utils.board_utils import *

def move_up(node, x, y):

    #Upwards movement
    if y != 0:
        for i in range(1, y + 1):
            if node.board[y - i][x] != BLANK_SPACE_CHAR:
                if i == 1:
                    break
                coords = (x, y - i + 1)
                return create_new_node(node, coords[0], coords[1], x, y)
            elif y - i == 0:
                coords = (x, y - i)
                return create_new_node(node, coords[0], coords[1], x, y)
    return None

def move_down(node, x, y):

    # Downwards movement
    if y != node.board_size - 1:
        for i in range(1, node.board_size - y):
            if node.board[y + i][x] != BLANK_SPACE_CHAR:
                if i == 1:
                    break
                coords = (x, y + i - 1)
                return create_new_node(node, coords[0], coords[1], x, y)
            elif y + i == node.board_size - 1:
                coords = (x, y + i)
                return create_new_node(node, coords[0], coords[1], x, y)
    return None

def move_left(node, x, y):

    # Left movement
    if x != 0:
        for i in range(1, x + 1):
            if node.board[y][x - i] != BLANK_SPACE_CHAR:
                if i == 1:
                    break
                coords = (x - i + 1, y)
                return create_new_node(node, coords[0], coords[1], x, y)
            elif x - i == 0:
                coords = (x - i, y)
                return create_new_node(node, coords[0], coords[1], x, y)
    return None

def move_right(node, x, y):

    # Right movement
    if x != node.board_size - 1:
        for i in range(1, node.board_size - x):
            if node.board[y][x + i] != BLANK_SPACE_CHAR:
                if i == 1:
                    break
                coords = (x + i - 1, y)
                return create_new_node(node, coords[0], coords[1], x, y)
            elif x + i == node.board_size - 1:
                coords = (x + i, y)
                return create_new_node(node, coords[0], coords[1], x, y)
    return None

def move_left_up(node,x, y):

    # Upwards-left movement
    if x != 0 and y != 0:
        limit = min([x + 1, y + 1])
        for i in range(1, limit):
            if node.board[y - i][x - i] != BLANK_SPACE_CHAR:
                if i == 1:
                    break
                coords = (x - i + 1, y - i + 1)
                return create_new_node(node, coords[0], coords[1], x, y)
            elif x - i == 0 or y - i == 0:
                coords = (x - i, y - i)
                return create_new_node(node, coords[0], coords[1], x, y)
    return None

def move_left_down(node, x, y):

    # Downwards-left movement
    if x != 0 and y != node.board_size - 1:
        limit = min([x + 1, node.board_size - y])
        for i in range(1, limit):
            if node.board[y + i][x - i] != BLANK_SPACE_CHAR:
                if i == 1:
                    break
                coords = (x - i + 1, y + i - 1)
                return create_new_node(node, coords[0], coords[1], x, y)
            elif x - i == 0 or y + i == node.board_size - 1:
                coords = (x - i, y + i)
                return create_new_node(node, coords[0], coords[1], x, y)
    return None

def move_right_up(node, x, y):

    # Upwards-right movement
    if x != node.board_size - 1 and y != 0:
        limit = min([node.board_size - x, y + 1])
        for i in range(1, limit):
            if node.board[y - i][x + i] != BLANK_SPACE_CHAR:
                if i == 1:
                    break
                coords = (x + i - 1, y - i + 1)
                return create_new_node(node, coords[0], coords[1], x, y)

            elif x + i == node.board_size - 1 or y - i == 0:
                coords = (x + i, y - i)
                return create_new_node(node, coords[0], coords[1], x, y)
    return None

def move_right_down(node, x, y):

    # Downwards-right movement
    if x != node.board_size - 1 and y != node.board_size - 1:
        limit = min([node.board_size - x, node.board_size - y])
        for i in range(1, limit):
            if node.board[y + i][x + i] != BLANK_SPACE_CHAR:
                if i == 1:
                    break
                coords = (x + i - 1, y + i - 1)
                return create_new_node(node, coords[0], coords[1], x, y)
            elif x + i == node.board_size - 1 or y + i == node.board_size - 1:
                coords = (x + i, y + i)
                return create_new_node(node, coords[0], coords[1], x, y)
    return None


def create_new_node(node, new_x, new_y, old_x, old_y):
    new_board = deepcopy(node.board)
    new_board[new_y][new_x] = new_board[old_y][old_x]
    new_board[old_y][old_x] = BLANK_SPACE_CHAR
    return Node(new_board, node.board_size)



operators = [
    move_up,
    move_down,
    move_left,
    move_right,
    move_left_up,
    move_left_down,
    move_right_up,
    move_right_down
]