import time
import random
from .node import *

# values for the termination of the game
BEST_VALUE_MINIMAX = 10000 # state value if the current player has won the game
WORST_VALUE_MINIMAX = -10000 # state value if the opponent player has won the game


def calculate_minimax(node, evaluator, first_turn, max_depth, player_char, opp_char):
    """
    Function that will calculate the best state from the current state,
    for the specified player, with a fixed max depth level.
    The depth first search of the minimax algorithm will be done
    recursively.
    """
    print("Computing minimax algorithm...")
    start_time = time.time()

    best_board, best_score = recursive_minimax((node, None, 0), evaluator, first_turn, max_depth, player_char, opp_char, True, float("-inf"), float("inf"))

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("The best play was calculated. Took {elapsed_time} s. (Score = {best_score})".format(elapsed_time=elapsed_time, best_score=best_score))

    new_node = Node(best_board, node.board_size)
    return new_node


def recursive_minimax(node_tuple, evaluator, first_turn, max_depth, player_char, opp_char, is_max_turn, alpha, beta):
    """
    Represents an "iteration" of the minimax algorithm.
    Alpha beta pruning and node ordering are implemented.
    Each node of the minimax tree is represented by the tuple (state, winner, score).
    State contains the board; winner contains the winner of the game (if any);
    score contains the score of the state, given the evaluator function.
    """
    # extract the node from the tuple
    node = node_tuple[0]

    # if the state should not be developed further, return its value.
    # This happens when the state if final (winner exists) or when
    # the maximum depth was reached.
    if node_tuple[1] is not None or node.depth == max_depth:
        return None, node_tuple[2]

    # calculate the player that has the current turn
    current_player = player_char if is_max_turn else opp_char

    # extract generator for the possible nodes
    gen = get_node_tuple_children(node, evaluator, player_char, current_player, first_turn)

    # if we are on the first state, calculate the possible nodes one by one,
    # to see if there is any final state. If there is, return it.
    # Else, keep them in a list to continue with the minimax algorithm.
    if node.depth == 0:
        possible_node_tuples = []
        for child_node_tuple in gen:
            if child_node_tuple[1] == player_char:
                return child_node_tuple[0].get_board(), child_node_tuple[2]

            possible_node_tuples.append(child_node_tuple)

    else:
        # calculate all children states
        possible_node_tuples = list(gen)

    # order the tuples by their score. If it is the maximizer's turn, by
    # decreasing order; if it is the minimizer's turn, by increasing order.
    # This is done to increase the probability of alpha-beta cuts.
    possible_node_tuples.sort(key = lambda x: x[2], reverse = is_max_turn)

    # initiate minimax variables
    best_score = float("-inf") if is_max_turn else float("inf")
    best_board = None

    # for each possible state
    for possible_node_tuple in possible_node_tuples:
        # extract the node from the tuple
        possible_node = possible_node_tuple[0]

        # recursively call minimax again on the possible node (depth first search)
        possible_node.set_parent(node)
        next_board, next_score = recursive_minimax(possible_node_tuple, evaluator, False, max_depth, player_char, opp_char, not is_max_turn, alpha, beta)

        # if the node is one that can be chosen has a the new board, instantiate the next_board variable
        if next_board == None and possible_node.depth == 1:
            next_board = possible_node.get_board()

        # if it is maximizer's turn, choose the highest value state
        if is_max_turn and best_score < next_score:
            best_score = next_score
            best_board = next_board
            alpha = max(alpha, best_score)
            # perform alpha-beta cut
            if beta <= alpha:
                break

        # if it is minimizer's turn, choose the lowest value state
        elif (not is_max_turn) and best_score > next_score:
            best_score = next_score
            best_board = next_board
            beta = min(beta, best_score)
            # perform alpha-beta cut
            if beta <= alpha:
                break


    return best_board, best_score


def get_node_tuple_children(node, evaluator, player_char, current_player, first_turn):
    """
    Function that calculates all possible children node tuples
    of the current node. Also calculates the score of the new nodes,
    and if they result in a winner or not (and which winner).
    """
    # if it is the first turn, move only a piece and not the neutron
    if first_turn:
        for i in range(node.board_size):
            for j in range(node.board_size):
                if ((current_player == PLAYER_A and node.get_board()[i][j] == PLAYER_A_SOLDIER_CHAR) or
                        (current_player == PLAYER_B and node.get_board()[i][j] == PLAYER_B_SOLDIER_CHAR)):
                    for op in operators:
                        new_board = op(node, j, i)
                        if new_board is not None:
                            new_node = Node(new_board, node.board_size)
                            _, winner = new_node.is_final_state_soldier(current_player)
                            score = calc_node_score(new_node, winner, evaluator, player_char)

                            yield (new_node, winner, score)
    else:
        neutron_x, neutron_y = node.get_neutron_coordinates()
        for op in operators:
            new_board = op(node, neutron_x, neutron_y)
            if new_board is not None:
                new_node = Node(new_board, node.board_size)
                end, winner = new_node.is_final_state_neutron()
                if end:
                    score = calc_node_score(new_node, winner, evaluator, player_char)

                    yield (new_node, winner, score)
                else:
                    for i in range(new_node.board_size):
                        for j in range(new_node.board_size):
                            if ((current_player == PLAYER_A and new_node.get_board()[i][j] == PLAYER_A_SOLDIER_CHAR) or
                                    (current_player == PLAYER_B and new_node.get_board()[i][j] == PLAYER_B_SOLDIER_CHAR)):
                                for op in operators:
                                    new_board = op(new_node, j, i)
                                    if new_board is not None:
                                        new_soldier_node = Node(new_board, node.board_size)
                                        _, winner = new_soldier_node.is_final_state_soldier(current_player)
                                        score = calc_node_score(new_soldier_node, winner, evaluator, player_char)

                                        yield (new_soldier_node, winner, score)



def calc_node_score(node, winner, evaluator, player_char):
    """
    Function that calculates the score of a node.
    """
    if winner == player_char:
        return BEST_VALUE_MINIMAX
    elif winner is None:
        return evaluator(node, player_char)
    else:
        return WORST_VALUE_MINIMAX