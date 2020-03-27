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

    best_board, best_score = recursive_minimax((node, None), evaluator, first_turn, max_depth, player_char, opp_char, True, float("-inf"), float("inf"))

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("The best play was calculated. Took {elapsed_time} s. (Score = {best_score})".format(elapsed_time=elapsed_time, best_score=best_score))

    new_node = Node(best_board, node.board_size)
    return new_node


def recursive_minimax(node_tuple, evaluator, first_turn, max_depth, player_char, opp_char, is_max_turn, alpha, beta):
    """
    Represents an "iteration" of the minimax algorithm.
    Alpha beta pruning is implemented.
    Returns the most advantageous play (column number) and its score.
    """
    # calculate the player that has the current turn
    current_player = player_char if is_max_turn else opp_char

    # if state is final, return its final value, depending on the current player
    winner = node_tuple[1]
    if winner == player_char:
        return None, BEST_VALUE_MINIMAX
    elif winner == opp_char:
        return None, WORST_VALUE_MINIMAX

    # extract the node from the tuple
    node = node_tuple[0]

    # check if the max depth has been reached
    if node.depth == max_depth:
        return None, evaluator(node, player_char)

    # extract generator for the possible nodes
    gen = get_node_pairs(node, current_player, first_turn)

    if node.depth == 0:
        # calculate the possible nodes one by one, to see if there is any final state.
        # If there is, return it. Else, keep them in a list to continue with the Minimax alg.
        possible_node_tuples = []
        for next_node_tuple in gen:
            if next_node_tuple[1] == player_char:
                return next_node_tuple[0].get_board(), BEST_VALUE_MINIMAX

            possible_node_tuples.append(next_node_tuple)

    else:
        # calculate all states
        possible_node_tuples = list(gen)

    # order the tuples
    random.shuffle(possible_node_tuples)  # TODO: node-ordering function


    # initiate minimax variables
    best_score = float("-inf") if is_max_turn else float("inf")
    best_board = None

    # for each possible state
    for possible_node_tuple in possible_node_tuples:
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
        for i in range(node.board_size):
            for j in range(node.board_size):
                if ((player_char == PLAYER_A and node.get_board()[i][
                    j] == PLAYER_A_SOLDIER_CHAR) or
                        (player_char == PLAYER_B and node.get_board()[i][
                            j] == PLAYER_B_SOLDIER_CHAR)):
                    for op in operators:
                        new_board = op(node, j, i)
                        if new_board is not None:
                            new_node = Node(new_board, node.board_size)
                            _, winner = new_node.is_final_state_soldier(player_char)
                            # print("Generated state 2: ")
                            # new_node.draw_node_in_terminal()
                            yield (new_node, winner)
    else:
        neutron_x, neutron_y = node.get_neutron_coordinates()
        for op in operators:
            new_board = op(node, neutron_x, neutron_y)
            if new_board is not None:
                new_node = Node(new_board, node.board_size)
                end, winner = new_node.is_final_state_neutron()
                if end:
                    # print("Generated state 1 : ")
                    # new_node.draw_node_in_terminal()
                    yield (new_node, winner)
                else:
                    for i in range(new_node.board_size):
                        for j in range(new_node.board_size):
                            if ((player_char == PLAYER_A and new_node.get_board()[i][
                                j] == PLAYER_A_SOLDIER_CHAR) or
                                    (player_char == PLAYER_B and new_node.get_board()[i][
                                        j] == PLAYER_B_SOLDIER_CHAR)):
                                for op in operators:
                                    new_board = op(new_node, j, i)
                                    if new_board is not None:
                                        new_soldier_node = Node(new_board, node.board_size)
                                        _, winner = new_soldier_node.is_final_state_soldier(player_char)
                                        # print("Generated state 2: ")
                                        # new_node.draw_node_in_terminal()
                                        yield (new_soldier_node, winner)



    # if first_turn:
    #     possible_neutron_nodes = [node]
    # else:
    #     possible_neutron_nodes = []
    #     neutron_x, neutron_y = node.get_neutron_coordinates()
    #     for op in operators:
    #         new_board = op(node, neutron_x, neutron_y)
    #         if new_board is not None:
    #             new_node = Node(new_board, node.board_size)
    #             end, winner = new_node.is_final_state_neutron()
    #             if end:
    #                 # print("Generated state 1 : ")
    #                 # new_node.draw_node_in_terminal()
    #                 yield (new_node, winner)
    #             else:
    #                 possible_neutron_nodes.append(new_node)
    #
    #
    # for possible_neutron_node in possible_neutron_nodes:
    #     for i in range(possible_neutron_node.board_size):
    #         for j in range(possible_neutron_node.board_size):
    #             if ((player_char == PLAYER_A and possible_neutron_node.get_board()[i][j] == PLAYER_A_SOLDIER_CHAR) or
    #                 (player_char == PLAYER_B and possible_neutron_node.get_board()[i][j] == PLAYER_B_SOLDIER_CHAR)):
    #                 for op in operators:
    #                     new_board = op(possible_neutron_node, j, i)
    #                     if new_board is not None:
    #                         new_node = Node(new_board, node.board_size)
    #                         _, winner = new_node.is_final_state_soldier(player_char)
    #                         # print("Generated state 2: ")
    #                         # new_node.draw_node_in_terminal()
    #                         yield (new_node, winner)


    # if first_turn:
    #     possible_neutron_nodes = [node]
    # else:
    #     possible_neutron_nodes = node.get_all_possible_nodes_for_player(player_char, True)
    #
    # possible_nodes = []
    # for possible_neutron_node in possible_neutron_nodes:
    #     end, winner = possible_neutron_node.is_final_state_neutron()
    #     if end:
    #         possible_nodes.append((possible_neutron_node, winner))
    #     else:
    #         possible_soldier_nodes = possible_neutron_node.get_all_possible_nodes_for_player(player_char, False)
    #         for possible_soldier_node in possible_soldier_nodes:
    #             _, winner = possible_soldier_node.is_final_state_soldier(player_char)
    #             possible_nodes.append((possible_soldier_node, winner))
    #
    # return possible_nodes

