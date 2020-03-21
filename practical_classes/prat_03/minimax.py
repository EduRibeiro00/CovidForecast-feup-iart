import time
import random

def calc_best_state_minimax(state, max_depth, player_char, opp_char):
    """
    Function that will calculate the best state from the current state,
    for the specified player, with a fixed max depth level.
    The depth first search of the minimax algorithm will be done
    recursively.
    """
    print("Computing minimax algorithm...")
    start_time = time.time()

    best_col, best_score = apply_minimax(state, 0, max_depth, player_char, opp_char, True, float("-inf"), float("inf"))

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("The best play is column {best_col}. Took {elapsed_time} s. (Score = {best_score})".format(best_col=best_col, elapsed_time=elapsed_time, best_score=best_score))
    return state.get_move_for_column(player_char, best_col)


def apply_minimax(state, cur_depth, max_depth, player_char, opp_char, is_max_turn, alpha, beta):
    """
    Represents an "iteration" of the minimax algorithm.
    Alpha beta pruning is implemented.
    Returns the most advantageous play (column number) and its score.
    """
    # check if the state is terminal
    end, winner = state.is_final_state()
    if end:
        if winner == player_char:
            return None, 1000
        elif winner == opp_char:
            return None, -1000
        else:
            return None, 0

    # check if the max depth has been reached
    if cur_depth == max_depth:
        return None, state.get_score(player_char)

    # calculate possible moves
    if is_max_turn:
        possible_states = state.get_possible_moves_for_player(player_char)
    else:
        possible_states = state.get_possible_moves_for_player(opp_char)

    best_score = float("-inf") if is_max_turn else float("inf")
    best_col = None
    random.shuffle(possible_states)

    for (possible_state, col_num) in possible_states:
        next_col, next_score = apply_minimax(possible_state, cur_depth + 1, max_depth, player_char, opp_char, not is_max_turn, alpha, beta)

        # if it is maximizer's turn, choose the highest value state
        if is_max_turn and best_score < next_score:
            best_score = next_score
            best_col = col_num
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break

        # if it is minimizer's turn, choose the lowest value state
        elif (not is_max_turn) and best_score > next_score:
            best_score = next_score
            best_col = col_num
            beta = min(beta, best_score)
            if beta <= alpha:
                break


    return best_col, best_score

