from utils.board_utils import *

def heuristic_function_simple(node, current_player):
    """
    Simple heuristic function, that takes into account the distance of the neutron
    to the player's first row, and the number of pieces surrounding the neutron.
    """
    alpha = 2
    beta = 1

    neutron_distance = 0
    surrounding_soldiers = 0

    for y in range(node.board_size):
        for x in range(node.board_size):

            if node.board[y][x] == NEUTRON_CHAR:

                # Calculates the distance between the neutron and the player's home rank
                if current_player == PLAYER_A:
                    neutron_distance = y
                else:
                    neutron_distance = node.board_size - y

                # Calculates the number of surrounding soldiers
                for j in range(-1, 2):
                    for i in range(-1, 2):

                        if x + i < 0 or x + i >= node.board_size or y + i < 0 or y + i >= node.board_size:
                            continue
                        elif node.board[y+j][x+i] == PLAYER_A_SOLDIER_CHAR or node.board[y+j][x+i] == PLAYER_B_SOLDIER_CHAR:
                            surrounding_soldiers += 1

    return alpha * neutron_distance + beta * surrounding_soldiers

