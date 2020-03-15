from state.game_state import GameState


class Menu:
    """
    Class that represents/handles the menus shown in the terminal,
    for the user to choose several parameters and aspects of the game.
    """
    def __init__(self):
        """
        Constructor of the class.
        """
        self.board_size = 5


    def get_board_size(self):
        """
        Returns the selected board size.
        """
        return self.board_size


    def handle_menu_state(self, state):
        """
        Depending on the current game state, shows the appropriate menu in the terminal
        and extracts user input.
        """
        if state == GameState.MAIN_MENU:
            new_state = self.show_main_menu()

        elif state == GameState.CHOOSE_BOARD_SIZE:
            new_state = self.show_choose_board_size_menu()

        # TODO: fazer os menus para os outros estados

        else:
            new_state = state

        return new_state


    def show_main_menu(self):
        """
        Method that shows the main menu to the user. Returns the new state for the game.
        """
        print('---------------------------------')
        print('       WELCOME TO NEUTRON!       ')
        print('---------------------------------')
        print('Choose an option:')
        print('1 -> Start a new game')
        print('2 -> Change board size')
        print('3 -> Exit the game')
        input = self.get_input_from_terminal([1, 2, 3])

        if input == 1:
            return GameState.PLAY_PREP
        elif input == 2:
            return GameState.CHOOSE_BOARD_SIZE
        elif input == 3:
            return GameState.EXIT


    def show_choose_board_size_menu(self):
        """
        Method that shows the board size menu to the user. Returns the new state for the game.
        """
        print('---------------------------------')
        print('Choose an option:')
        print('1 -> 5 x 5')
        print('2 -> 7 x 7')
        print('3 -> 11 x 11')
        print('Current: {size} x {size}'.format(size=self.board_size))
        input = self.get_input_from_terminal([1, 2, 3])

        if input == 1:
            self.board_size = 5
        elif input == 2:
            self.board_size = 7
        elif input == 3:
            self.board_size = 11

        return GameState.MAIN_MENU


    def get_input_from_terminal(self, accepted_inputs):
        """
        Function that reads from the terminal and waits for the user to input
        an option. Verifies if that option is in the accepted inputs.
        """
        global input
        while True:
            option = input('Option: ')
            try:
                option = int(option)
                if option in accepted_inputs:
                    return option
                else:
                    print('The input is invalid. Please try again.')
                    continue

            except ValueError:
                print('The input is invalid. Please try again.')
                continue




