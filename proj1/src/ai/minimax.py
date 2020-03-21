import time
import random
from .node import *

def calculate_minimax(node, evaluator, first_turn, max_depth, player_char, opp_char):
    """
    Function that will calculate the best state from the current state,
    for the specified player, with a fixed max depth level.
    The depth first search of the minimax algorithm will be done
    recursively.
    """

    print("Computing minimax algorithm...")
    start_time = time.time()

    best_board, best_score = recursive_minimax(node, evaluator, first_turn, max_depth, player_char, opp_char, True, float("-inf"), float("inf"))

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("The best play is column {best_board}. Took {elapsed_time} s. (Score = {best_score})".format(best_board=best_board, elapsed_time=elapsed_time, best_score=best_score))

    new_node = Node(best_board, node.board_size)
    return new_node



def recursive_minimax(node, evaluator, first_turn, max_depth, player_char, opp_char, is_max_turn, alpha, beta):
    """
    Represents an "iteration" of the minimax algorithm.
    Alpha beta pruning is implemented.
    Returns the most advantageous play (column number) and its score.
    """
    # check if the node is terminal
    end, winner = node.is_final_state(player_char)
    if end:
        if winner == player_char:
            return deepcopy(node.board), 10000
        else:
            return deepcopy(node.board), -10000

    # check if the max depth has been reached
    if node.depth == max_depth:
        return deepcopy(node.board), evaluator(node, player_char)

    # calculate possible moves
    if is_max_turn:
        possible_nodes = get_node_pairs(node, player_char, first_turn)
    else:
        possible_nodes = get_node_pairs(node, opp_char, first_turn)

    best_score = float("-inf") if is_max_turn else float("inf")
    best_board = None
    random.shuffle(possible_nodes) #TODO: node-ordering function

    for possible_node in possible_nodes:
        possible_node.set_parent(node)
        next_board, next_score = recursive_minimax(possible_node, evaluator, False, max_depth, player_char, opp_char, not is_max_turn, alpha, beta)

        # if it is maximizer's turn, choose the highest value state
        if is_max_turn and best_score < next_score:
            best_score = next_score
            best_board = next_board
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break

        # if it is minimizer's turn, choose the lowest value state
        elif (not is_max_turn) and best_score > next_score:
            best_score = next_score
            best_board = next_board
            beta = min(beta, best_score)
            if beta <= alpha:
                break

    return best_board, best_score



def get_node_pairs(node, player_char, first_turn):
    if first_turn:
        possible_neutron_nodes = [node]

    else:
        possible_neutron_nodes = node.get_all_possible_nodes_for_player(player_char, True)

    possible_nodes = []
    for possible_neutron_node in possible_neutron_nodes:
        possible_soldier_nodes = possible_neutron_node.get_all_possible_nodes_for_player(player_char, False)
        possible_nodes = possible_nodes + possible_soldier_nodes

    return possible_nodes

