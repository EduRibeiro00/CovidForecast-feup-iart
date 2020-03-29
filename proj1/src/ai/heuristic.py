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
    Medium heuristic function, that takes into account the distance of the neutron
    to the player's first row, and the number of pieces surrounding the neutron.
    """
    alpha = 25
    beta = 10
    gamma = 40
    delta = -200

    x, y = node.get_neutron_coordinates()

    # Calculates the distance between the neutron and the player's home rank
    # and calculates how many paths exist for the neutron to reach the player's home rank
    # as well as for the opponent
    if current_player == PLAYER_A:
        neutron_distance = y

        player_paths = get_number_of_paths(node, x, y, PLAYER_A)
        opponent_paths = get_number_of_paths(node, x, y, PLAYER_B)

    else:
        neutron_distance = node.board_size - y

        player_paths = get_number_of_paths(node, x, y, PLAYER_B)
        opponent_paths = get_number_of_paths(node, x, y, PLAYER_A)                                          

    surrounding_soldiers = 0

    # Calculates the number of surrounding soldiers
    for j in range(-1, 2):
        for i in range(-1, 2):

            if x + i < 0 or x + i >= node.board_size or y + j < 0 or y + j >= node.board_size:
                continue
            elif node.board[y+j][x+i] == PLAYER_A_SOLDIER_CHAR or node.board[y+j][x+i] == PLAYER_B_SOLDIER_CHAR:
                surrounding_soldiers += 1

    return alpha*neutron_distance + beta*surrounding_soldiers + gamma*player_paths + delta*opponent_paths 




def get_number_of_paths(node, x, y, current_player):
    """
    Calculates the number of possible paths for the neutron to reach
    the player's home rank
    """
    paths = 0

    if current_player == PLAYER_A:
        # Possible downwards path
        if y != node.board_size - 1:
            for i in range(1, node.board_size - y):
                if node.board[y+i][x] != BLANK_SPACE_CHAR :
                    break
                elif y + i == node.board_size - 1:                 
                    paths += 1
                    break  

        # Possible downwards-right path
        if x != node.board_size - 1 and y != node.board_size - 1:
            limit = min([node.board_size - x, node.board_size - y])
            for i in range(1, limit):
                if node.board[y+i][x+i] != BLANK_SPACE_CHAR:
                    break 
                elif y + i == node.board_size - 1:   
                    paths += 1
                    break     

        # Possible downwards-left path
        if x != 0 and y != node.board_size - 1:
            limit = min([x + 1, node.board_size - y])
            for i in range(1, limit):
                if node.board[y+i][x-i] != BLANK_SPACE_CHAR:
                    break 
                elif y + i == node.board_size - 1:                  
                    paths += 1
                    break  

    else:
        # Possible upwards path
        if y != 0:
            for i in range(1, y + 1):
                if node.board[y- i][x] != BLANK_SPACE_CHAR:
                    break 
                elif y - i == 0:                   
                    paths += 1
                    break 

        # Possible upwards-right path
        if x != node.board_size - 1 and y != 0:
            limit = min([node.board_size - x, y + 1])
            for i in range(1, limit):
                if node.board[y-i][x+i] != BLANK_SPACE_CHAR:
                    break 
                elif x + i == node.board_size - 1 or y - i == 0:                  
                    paths += 1
                    break 

        # Possible upwards-left path
        if x != 0 and y != 0:
            limit = min([x + 1, y + 1])
            for i in range(1, limit):
                if node.board[y-i][x-i] != BLANK_SPACE_CHAR:
                    break  
                elif x - i == 0 or y - i == 0:                  
                    paths += 1
                    break 

    return paths   
