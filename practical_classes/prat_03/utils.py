def create_initial_board():
    board = []
    for i in range(6): # 6 cells of height
        line = []
        for j in range(7): # 7 cells of width
            line.append(' ')
        board.append(line)

    return board


def select_move_from_player(state, player_char):
    while True:
        valid_input = True
        try:
            col = int(input("Select a column for the next play: "))
            new_state = state.get_move_for_column(player_char, col)
            if new_state is None:
                valid_input = False

        except ValueError:
            valid_input = False

        if valid_input:
            break
        else:
            print()
            print('Invalid option. Please try again.')

    return new_state
