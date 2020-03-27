from utils.board_utils import *

def heuristic_function_easy(node, current_player):
    """
    Simple heuristic function.
    """
    _, y = node.get_neutron_coordinates()

    # Calculates the distance between the neutron and the player's home rank
    if current_player == PLAYER_A:
        return y
    else:
        return node.board_size - y




def heuristic_function_medium(node, current_player):
    """
    Medium heuristic function, that takes into account the distance of the neutron
    to the player's first row, and the number of pieces surrounding the neutron.
    """
    alpha = 25
    beta = 10

    x, y = node.get_neutron_coordinates()

    # Calculates the distance between the neutron and the player's home rank
    if current_player == PLAYER_A:
        neutron_distance = y
    else:
        neutron_distance = node.board_size - y

    surrounding_soldiers = 0

    # Calculates the number of surrounding soldiers
    for j in range(-1, 2):
        for i in range(-1, 2):

            if x + i < 0 or x + i >= node.board_size or y + j < 0 or y + j >= node.board_size:
                continue
            elif node.board[y+j][x+i] == PLAYER_A_SOLDIER_CHAR or node.board[y+j][x+i] == PLAYER_B_SOLDIER_CHAR:
                surrounding_soldiers += 1


    return alpha * neutron_distance + beta * surrounding_soldiers




def heuristic_function_hard(node, current_player):
    """
    More complex heuristic function.
    """
    # TODO
    pass

