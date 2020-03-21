from prat_03.minimax import calc_best_state_minimax
from prat_03.state import State
from prat_03.utils import create_initial_board
from prat_03.utils import select_move_from_player

def main(player_X, player_O):
    """
    Main of the game.
    """
    current_state = State(create_initial_board())
    current_player = 'X'
    max_depth = 4

    while True:
        print()
        current_state.print_state()
        print()

        end, winner = current_state.is_final_state()
        if end:
            if winner == '':
                print('It was a draw!')
            else:
                print('And the winner is {winner}!'.format(winner=winner))
            break

        new_state = None

        if current_player == 'X':
            opp_player = 'O'
            if player_X == 'H':
                new_state = select_move_from_player(current_state, current_player)
            else:
                new_state = calc_best_state_minimax(current_state, max_depth, current_player, opp_player)

        if current_player == 'O':
            opp_player = 'X'
            if player_O == 'H':
                new_state = select_move_from_player(current_state, current_player)
            else:
                new_state = calc_best_state_minimax(current_state, max_depth, current_player, opp_player)

        current_state = new_state

        if current_player == 'X':
            current_player = 'O'
        else:
            current_player = 'X'


if __name__ == '__main__':
    main('H', 'C')