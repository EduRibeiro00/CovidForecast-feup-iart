from state.game_state import GameState

HUMAN_VS_HUMAN = "H / H"
COMPUTER_VS_HUMAN = "C / H"
COMPUTER_VS_COMPUTER = "C / C"
HUMAN_VS_COMPUTER = "H / C"

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
        self.difficulty_player_a = 'Medium'
        self.difficulty_player_b = 'Medium'
        self.game_mode = 'H / C'


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

        elif state == GameState.CHOOSE_DIFFICULTY_A:
            new_state = self.show_difficulty_menu('a')

        elif state == GameState.CHOOSE_DIFFICULTY_B:
            new_state = self.show_difficulty_menu('b')

        elif state == GameState.MODE_SELECT:
            new_state = self.show_mode_select_menu()

        elif state == GameState.INSTRUCTIONS:
            new_state = self.show_instructions_menu()

        elif state == GameState.GAME_OVER:
            new_state = self.show_game_over_menu()

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
        print('3 -> Mode select')
        print('4 -> Choose AI difficulty for player A')
        print('5 -> Choose AI difficulty for player B')
        print('6 -> See instructions')
        print('7 -> Exit the game')
        input = self.get_input_from_terminal([1, 2, 3, 4, 5, 6, 7])

        if input == 1:
            return GameState.PLAY_PREP
        elif input == 2:
            return GameState.CHOOSE_BOARD_SIZE
        elif input == 3:
            return GameState.MODE_SELECT
        elif input == 4:
            return GameState.CHOOSE_DIFFICULTY_A
        elif input == 5:
            return GameState.CHOOSE_DIFFICULTY_B
        elif input == 6:
            return GameState.INSTRUCTIONS
        elif input == 7:
            return GameState.EXIT


    def show_game_over_menu(self):
        """
        Method that shows the game over menu to the user. Returns the new state for the game.
        """
        print('---------------------------------')
        print('GAME OVER!')
        print('Choose an option:')
        print('1 -> Start a new game')
        print('2 -> Return to Main Menu')
        input = self.get_input_from_terminal([1, 2])

        if input == 1:
            return GameState.PLAY_PREP
        elif input == 2:
            return GameState.MAIN_MENU


    def show_instructions_menu(self):
        """
        Method that shows the instructions menu to the user. Returns the new state for the game.
        """
        print('------------------------------------------')
        print('INSTRUCTIONS:')
        print('Neutron is a two player game, normally played in a 5x5 board, although this game features boards of various sizes.')
        print('The goal of each player is to bring the Neutron to their home rank (the first row on their side of the board).')
        print('The player can either bring the Neutron to their home rank during their turn, or have the other player')
        print('bring it over there which only normally happens if forced upon during their turn. The other way to win, is')
        print('to stalemate the other player, that is, by not allowing the other player complete their turn which consists')
        print('of moving the Neutron first, and then one of their soldiers (except on the first player\'s first turn,')
        print('where they can only move a soldier).')
        print()
        print('A soldier moves in a straight line (orthogonal or diagonal). It must move as far as it can; so it')
        print('continues until it finds an edge or another piece. There is no capturing.')
        print('The neutron moves like the soldier.')
        print('As previously said, each player first moves the neutron, then one of his soldiers.')
        print('On the first turn of the game, the first player does not move the neutron.')
        print('------------------------------------------')
        print('Press 1 to return to the Main Menu.')
        input = self.get_input_from_terminal([1])

        if input == 1:
            return GameState.MAIN_MENU


    def show_difficulty_menu(self, player):
        """
        Method that shows the difficulty menu (for the specified player) to the user. Returns the new state for the game.
        """
        print('---------------------------------')
        print('Choose an option:')
        print('1 -> Easy')
        print('2 -> Medium')
        print('3 -> Hard')
        if player == 'a':
            diff = self.difficulty_player_a
        else:
            diff = self.difficulty_player_b

        print('Current: {diff}'.format(diff=diff))
        input = self.get_input_from_terminal([1, 2, 3])

        if input == 1:
            difficulty = 'Easy'
        elif input == 2:
            difficulty = 'Medium'
        else:
            difficulty = 'Hard'

        if player == 'a':
            self.difficulty_player_a = difficulty
        else:
            self.difficulty_player_b = difficulty

        return GameState.MAIN_MENU


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


    def show_mode_select_menu(self):
        """
        Method that shows the mode select menu to the user. Returns the new state for the game.
        """
        print('---------------------------------')
        print('Choose an option:')
        print('1 -> H / H')
        print('2 -> H / C')
        print('3 -> C / C')
        print('Current: {mode}'.format(mode=self.game_mode))
        input = self.get_input_from_terminal([1, 2, 3])

        if input == 1:
            self.game_mode = 'H / H'
        elif input == 2:
            self.game_mode = 'H / C'
        elif input == 3:
            self.game_mode = 'C / C'

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




