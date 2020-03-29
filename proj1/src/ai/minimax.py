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
    Gets a score hashmap containing the pre-calculated scores for some states.
    Also updates this hashmap for values missing.
    """
    print("Computing minimax algorithm...")
    start_time = time.time()

    scores_cache = {}

    best_board, best_score = recursive_minimax((node, None), scores_cache, evaluator, first_turn, max_depth, player_char, opp_char, True, float("-inf"), float("inf"))
    print("Cache has {} entries.".format(len(scores_cache)))

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("The best play was calculated. Took {elapsed_time} s. (Score = {best_score})".format(elapsed_time=elapsed_time, best_score=best_score))

    new_node = Node(best_board, node.board_size)
    return new_node


def recursive_minimax(node_tuple, scores_cache, evaluator, first_turn, max_depth, player_char, opp_char, is_max_turn, alpha, beta):
    """
    Represents an "iteration" of the minimax algorithm.
    Alpha beta pruning and node ordering are implemented.
    Each node of the minimax tree is represented by the tuple (state, winner).
    State contains the board; winner contains the winner of the game (if any).
    """
    # extract the node and the winner from the tuple
    node = node_tuple[0]
    winner = node_tuple[1]

    # calculate the player that has the current turn
    current_player = player_char if is_max_turn else opp_char

    key = str((node.get_board(), node.depth, player_char))
    # check if the score of the current node was already calculated
    # and is being kept in cache
    if key in scores_cache:
        # print("Cache was used.")
        return None, scores_cache[key]

    # if the state should not be developed further, return its value.
    # This happens when the state if final (winner exists) or when
    # the maximum depth was reached.
    if winner == player_char:
        score = BEST_VALUE_MINIMAX
        # store the score value in the cache
        scores_cache[key] = score
        return None, score
    elif winner == opp_char:
       score = WORST_VALUE_MINIMAX
       # store the score value in the cache
       scores_cache[key] = score
       return None, score
    elif node.depth == max_depth:
        score = evaluator(node, player_char)
        # store the score value in the cache
        scores_cache[key] = score
        return None, score


    # extract generator for the possible nodes
    gen = get_node_tuple_children(node, current_player, first_turn)

    # if we are on the first state, calculate the possible nodes one by one,
    # to see if there is any final state. If there is, return it.
    # Else, keep them in a list to continue with the minimax algorithm.
    if node.depth == 0:
        possible_node_tuples = []
        for child_node_tuple in gen:
            if child_node_tuple[1] == player_char:
                scores_cache[key] = BEST_VALUE_MINIMAX
                return child_node_tuple[0].get_board(), BEST_VALUE_MINIMAX

            possible_node_tuples.append(child_node_tuple)

    else:
        # generator for all possible states, in order to calculate them one by one
        possible_node_tuples = gen


    # initiate minimax variables
    best_score = float("-inf") if is_max_turn else float("inf")
    best_board = None

    # for each possible state
    for possible_node_tuple in possible_node_tuples:
        # extract the node from the tuple
        possible_node = possible_node_tuple[0]

        # recursively call minimax again on the possible node (depth first search)
        possible_node.set_parent(node)
        next_board, next_score = recursive_minimax(possible_node_tuple, scores_cache, evaluator, False, max_depth, player_char, opp_char, not is_max_turn, alpha, beta)

        # if the node is one that can be chosen has a the new board, instantiate the next_board variable
        if possible_node.depth == 1:
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

    # store the score value in cache
    scores_cache[key] = best_score
    return best_board, best_score


def get_node_tuple_children(node, current_player, first_turn):
    """
    Function that calculates all possible children node tuples
    of the current node. Also calculates if they result in a winner
    or not (and which winner).
    In order to avoid calculating all children nodes at once,
    the function uses the yield keyword, returning a generator instead
    of the whole result. This way, the nodes are only generated one by one.
    Alpha-beta cuts are more efficient this way.
    """
    # if it is the first turn, move only a piece and not the neutron
    if first_turn:
        for i in range(node.board_size):
            for j in range(node.board_size):
                # if the board cell contains a piece of the player
                if ((current_player == PLAYER_A and node.get_board()[i][j] == PLAYER_A_SOLDIER_CHAR) or
                        (current_player == PLAYER_B and node.get_board()[i][j] == PLAYER_B_SOLDIER_CHAR)):
                    # calculate all states generated by moving that piece
                    for op in operators:
                        new_board = op(node, j, i)
                        if new_board is not None:
                            new_node = Node(new_board, node.board_size)
                            _, winner = new_node.is_final_state_soldier(current_player)
                            yield (new_node, winner)
    else:
        neutron_x, neutron_y = node.get_neutron_coordinates()
        # calculate all states generated by moving the neutron
        for op in operators:
            new_board = op(node, neutron_x, neutron_y)
            if new_board is not None:
                new_node = Node(new_board, node.board_size)
                end, winner = new_node.is_final_state_neutron()
                # if the state is already final, don't move a piece
                if end:
                    yield (new_node, winner)
                else:
                    for i in range(new_node.board_size):
                        for j in range(new_node.board_size):
                            # if the board cell contains a piece of the player
                            if ((current_player == PLAYER_A and new_node.get_board()[i][j] == PLAYER_A_SOLDIER_CHAR) or
                                    (current_player == PLAYER_B and new_node.get_board()[i][j] == PLAYER_B_SOLDIER_CHAR)):
                                # calculate all states generated by moving that piece
                                for op in operators:
                                    new_board = op(new_node, j, i)
                                    if new_board is not None:
                                        new_soldier_node = Node(new_board, node.board_size)
                                        _, winner = new_soldier_node.is_final_state_soldier(current_player)
                                        yield (new_soldier_node, winner)