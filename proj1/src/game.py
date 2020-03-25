from interface.menu import *
from utils.board_utils import *
from interface.game_interface import GameInterface
from state.game_state import GameState
from state.play_state import PlayState
from ai.minimax import *
from ai.heuristic import *

import time




class Game:
    """
    Main class representing the game.
    """
    def __init__(self):
        """
        Constructor of the class.
        """
        self.menu = Menu()
        self.interface = GameInterface()
        self.game_state = GameState.MAIN_MENU
        self.play_state = PlayState.PLAYER_A_CHOOSING_SOLDIER
        self.selected_piece_x = None
        self.selected_piece_y = None
        self.current_player = PLAYER_A
        self.first_turn = True



    def adapt_to_board_size(self):
        """
        Method that adapts the needed parameters/variables to the selected board size.
        """
        self.size = self.menu.get_board_size()
        self.current_board = create_initial_board(self.size) # create board with the wanted size


    def test_minimax(self):
        self.adapt_to_board_size()

        board = [['B', 'B', 'B', 'B', 'B'],
                 [' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', 'W', 'N'],
                 ['W', 'W', 'W', 'W', ' '],]

        node = Node(board, self.size)
        current_node = Node(self.current_board, self.size)

        current_node.draw_node_in_terminal()
        node.draw_node_in_terminal()



        print(determine_moves_neutron_soldier(self.current_board, board, self.size))

        #new_node =  calculate_minimax(node, heuristic_function_simple, False, 5, PLAYER_A, PLAYER_B)

        # new_node.draw_node_in_terminal()



    def run(self):
        """
        Main method of the game class. Contains the main game cycle.
        """

        while self.game_state != GameState.EXIT:

            if self.game_state == GameState.PLAY_PREP:
                self.adapt_to_board_size()
                self.interface.start_interface(self.size)
                self.play_state = PlayState.PLAYER_A_CHOOSING_SOLDIER
                self.game_state = GameState.PLAY
                self.first_turn = True


            elif self.game_state == GameState.PLAY:


                if self.play_state == PlayState.PLAYER_A_WINS or self.play_state == PlayState.PLAYER_B_WINS:
                    self.interface.draw_board(self.current_board)
                    self.interface.display_turn_information(self.play_state)
                    self.interface.flip()
                    self.play_state = PlayState.END

                elif self.play_state != PlayState.END:
                    self.interface.draw_board(self.current_board)
                    self.interface.display_turn_information(self.play_state)
                    self.interface.flip()

                    if self.menu.game_mode == HUMAN_VS_HUMAN:
                        self.process_events()

                    elif self.menu.game_mode == HUMAN_VS_COMPUTER:
                        if self.current_player == PLAYER_A:
                            self.process_events()
                        elif self.current_player == PLAYER_B:
                            self.make_move_ai()

                    elif self.menu.game_mode == COMPUTER_VS_HUMAN:
                        if self.current_player == PLAYER_A:
                            self.make_move_ai()
                        elif self.current_player == PLAYER_B:
                            self.process_events()

                    elif self.menu.game_mode == COMPUTER_VS_COMPUTER:
                        self.make_move_ai()



                else: # end play state

                    # to give time for the player to see which player has won the game
                    time.sleep(2.5)
                    self.interface.end_game()
                    self.game_state = GameState.GAME_OVER


            elif self.game_state != GameState.EXIT:
                self.game_state = self.menu.handle_menu_state(self.game_state)


    def process_events(self):
        """
        Method that processes events from the interface.
        """
        event_queue = self.interface.watch_for_events()  # get events from pygame

        for event in event_queue:
            # quit the game
            if event == 'EVENT_QUIT':
                self.play_state = PlayState.END

            # if the mouse button was pressed
            elif event == 'EVENT_MOUSEBUTTONDOWN':
                self.handle_mouse_event()


    def handle_mouse_event(self):
        """
        Method that handles all the events coming from the mouse.
        """
        if self.game_state == GameState.PLAY:

            # mouse coordinates
            square = self.interface.check_collision()

            if square is not None:
                # represents the columns
                x = square.x
                # represents the rows
                y = square.y
                if self.play_state == PlayState.PLAYER_A_CHOOSING_SOLDIER:
                    if self.current_board[y][x] == PLAYER_A_SOLDIER_CHAR:
                        self.interface.set_selected_square(x, y)
                        self.selected_piece_x = x
                        self.selected_piece_y = y
                        self.play_state = PlayState.PLAYER_A_MOVING_SOLDIER
                        self.highlights = self.possible_moves(x, y)
                        self.interface.highlight_squares(self.highlights)

                elif self.play_state == PlayState.PLAYER_A_MOVING_SOLDIER:

                    if self.current_board[y][x] == BLANK_SPACE_CHAR and (x,y) in self.highlights:
                        self.interface.unset_selected_square(self.selected_piece_x, self.selected_piece_y)
                        self.current_board[self.selected_piece_y][self.selected_piece_x] = BLANK_SPACE_CHAR
                        self.current_board[y][x] = PLAYER_A_SOLDIER_CHAR
                        game_over_bool, final_state = self.check_game_end()
                        if game_over_bool:
                            self.play_state = final_state
                        else:
                            self.play_state = PlayState.PLAYER_B_CHOOSING_NEUTRON
                            self.current_player = PLAYER_B
                            if self.first_turn:
                                self.first_turn = False
                        self.interface.reset_highlight()

                    elif self.current_board[y][x] == PLAYER_A_SOLDIER_CHAR:
                        self.interface.unset_selected_square(self.selected_piece_x, self.selected_piece_y)
                        self.interface.set_selected_square(x, y)
                        self.selected_piece_x = x
                        self.selected_piece_y = y
                        self.interface.reset_highlight()
                        self.highlights = self.possible_moves(x, y)
                        self.interface.highlight_squares(self.highlights)                        

                elif self.play_state == PlayState.PLAYER_A_CHOOSING_NEUTRON:
                    if self.current_board[y][x] == NEUTRON_CHAR:
                        self.interface.set_selected_square(x, y)
                        self.selected_piece_x = x
                        self.selected_piece_y = y
                        self.play_state = PlayState.PLAYER_A_MOVING_NEUTRON
                        self.highlights = self.possible_moves(x, y)
                        self.interface.highlight_squares(self.highlights)                        

                elif self.play_state == PlayState.PLAYER_A_MOVING_NEUTRON:
                    if self.current_board[y][x] == BLANK_SPACE_CHAR and (x,y) in self.highlights:
                        self.interface.unset_selected_square(self.selected_piece_x, self.selected_piece_y)
                        self.current_board[self.selected_piece_y][self.selected_piece_x] = BLANK_SPACE_CHAR
                        self.current_board[y][x] = NEUTRON_CHAR
                        game_over_bool, final_state = self.check_game_end()
                        if game_over_bool:
                            self.play_state = final_state
                        else:
                            self.play_state = PlayState.PLAYER_A_CHOOSING_SOLDIER
                        self.interface.reset_highlight()

                elif self.play_state == PlayState.PLAYER_B_CHOOSING_SOLDIER:
                    if self.current_board[y][x] == PLAYER_B_SOLDIER_CHAR:
                        self.interface.set_selected_square(x, y)
                        self.selected_piece_x = x
                        self.selected_piece_y = y
                        self.play_state = PlayState.PLAYER_B_MOVING_SOLDIER
                        self.highlights = self.possible_moves(x, y)
                        self.interface.highlight_squares(self.highlights)

                elif self.play_state == PlayState.PLAYER_B_MOVING_SOLDIER:
                    if self.current_board[y][x] == BLANK_SPACE_CHAR and (x,y) in self.highlights:
                        self.interface.unset_selected_square(self.selected_piece_x, self.selected_piece_y)
                        self.current_board[self.selected_piece_y][self.selected_piece_x] = BLANK_SPACE_CHAR
                        self.current_board[y][x] = PLAYER_B_SOLDIER_CHAR
                        game_over_bool, final_state = self.check_game_end()
                        if game_over_bool:
                            self.play_state = final_state
                        else:
                            self.play_state = PlayState.PLAYER_A_CHOOSING_NEUTRON
                            self.current_player = PLAYER_B
                        self.interface.reset_highlight()
                    elif self.current_board[y][x] == PLAYER_B_SOLDIER_CHAR:
                        self.interface.unset_selected_square(self.selected_piece_x, self.selected_piece_y)
                        self.interface.set_selected_square(x, y)
                        self.selected_piece_x = x
                        self.selected_piece_y = y
                        self.interface.reset_highlight()                        
                        self.highlights = self.possible_moves(x, y)
                        self.interface.highlight_squares(self.highlights)    

                elif self.play_state == PlayState.PLAYER_B_CHOOSING_NEUTRON:
                    if self.current_board[y][x] == NEUTRON_CHAR:
                        self.interface.set_selected_square(x, y)
                        self.selected_piece_x = x
                        self.selected_piece_y = y
                        self.play_state = PlayState.PLAYER_B_MOVING_NEUTRON
                        self.highlights = self.possible_moves(x, y)
                        self.interface.highlight_squares(self.highlights)               

                elif self.play_state == PlayState.PLAYER_B_MOVING_NEUTRON:
                    if self.current_board[y][x] == BLANK_SPACE_CHAR and (x,y) in self.highlights:
                        self.interface.unset_selected_square(self.selected_piece_x, self.selected_piece_y)
                        self.current_board[self.selected_piece_y][self.selected_piece_x] = BLANK_SPACE_CHAR
                        self.current_board[y][x] = NEUTRON_CHAR
                        game_over_bool, final_state = self.check_game_end()
                        if game_over_bool:
                            self.play_state = final_state
                        else:
                            self.play_state = PlayState.PLAYER_B_CHOOSING_SOLDIER
                        self.interface.reset_highlight()                  



    def possible_moves(self, x, y):
        """
        Method that calculates all possible movements of a given piece.
        """
        possibilities = []
        
        # Right movement
        if x != self.size - 1:
            for i in range(1, self.size - x):
                if self.current_board[y][x+i] != BLANK_SPACE_CHAR:
                    if i == 1:
                        break
                    coords = (x+i-1, y)
                    possibilities.append(coords)
                    break
                elif x + i == self.size - 1:
                    coords = (x+i, y)
                    possibilities.append(coords)
                    break      

        # Left movement
        if x != 0:
            for i in range(1, x + 1):
                if self.current_board[y][x-i] != BLANK_SPACE_CHAR:
                    if i == 1:
                        break
                    coords = (x-i+1, y)
                    possibilities.append(coords)
                    break
                elif x - i == 0:
                    coords = (x-i, y)
                    possibilities.append(coords)
                    break

        # Downwards movement
        if y != self.size - 1:
            for i in range(1, self.size - y):
                if self.current_board[y+i][x] != BLANK_SPACE_CHAR:
                    if i == 1:
                        break                    
                    coords = (x, y+i-1)
                    possibilities.append(coords)
                    break
                elif y + i == self.size - 1:                 
                    coords = (x, y+i)
                    possibilities.append(coords)
                    break               

        # Upwards movement
        if y != 0:
            for i in range(1, y + 1):
                if self.current_board[y- i][x] != BLANK_SPACE_CHAR:
                    if i == 1:
                        break                    
                    coords = (x, y-i+1)
                    possibilities.append(coords)
                    break 
                elif y - i == 0:                   
                    coords = (x, y-i)
                    possibilities.append(coords)
                    break                  

        # Downwards-right movement
        if x != self.size - 1 and y != self.size - 1:
            limit = min([self.size - x, self.size - y])
            for i in range(1, limit):
                if self.current_board[y+i][x+i] != BLANK_SPACE_CHAR:
                    if i == 1:
                        break
                    coords = (x+i-1, y+i-1)
                    possibilities.append(coords)
                    break 
                elif x + i == self.size - 1 or y + i == self.size - 1:   
                    coords = (x+i, y+i)
                    possibilities.append(coords)
                    break                

        # Upwards-right movement
        if x != self.size - 1 and y != 0:
            limit = min([self.size - x, y + 1])
            for i in range(1, limit):
                if self.current_board[y-i][x+i] != BLANK_SPACE_CHAR:
                    if i == 1:
                        break                    
                    coords = (x+i-1, y-i+1)
                    possibilities.append(coords)
                    break 
                elif x + i == self.size - 1 or y - i == 0:                  
                    coords = (x+i, y-i)
                    possibilities.append(coords)
                    break                

        # Downwards-left movement
        if x != 0 and y != self.size - 1:
            limit = min([x + 1, self.size - y])
            for i in range(1, limit):
                if self.current_board[y+i][x-i] != BLANK_SPACE_CHAR:
                    if i == 1:
                        break                    
                    coords = (x-i+1, y+i-1)
                    possibilities.append(coords)
                    break 
                elif x - i == 0 or y + i == self.size - 1:                  
                    coords = (x-i, y+i)
                    possibilities.append(coords)
                    break                                   

        # Upwards-left movement
        if x != 0 and y != 0:
            limit = min([x + 1, y + 1])
            for i in range(1, limit):
                if self.current_board[y-i][x-i] != BLANK_SPACE_CHAR:
                    if i == 1:
                        break                    
                    coords = (x-i+1, y-i+1)
                    possibilities.append(coords)
                    break  
                elif x - i == 0 or y - i == 0:                  
                    coords = (x-i, y-i)
                    possibilities.append(coords)
                    break                                     

        return possibilities

    def make_move_ai(self):

        node = Node(self.current_board, self.size)

        if self.current_player == PLAYER_B:
            opponent_player = PLAYER_A
            player_piece = PLAYER_B_SOLDIER_CHAR
        elif self.current_player == PLAYER_A:
            opponent_player = PLAYER_B
            player_piece = PLAYER_A_SOLDIER_CHAR

        new_node =  calculate_minimax(node, heuristic_function_simple, self.first_turn, 3, self.current_player, opponent_player)

        node.draw_node_in_terminal()
        node_board_actual = Node(self.current_board, self.size)
        node_board_actual.draw_node_in_terminal()
        new_node.draw_node_in_terminal()

        neutron, soldier = determine_moves_neutron_soldier(self.current_board, new_node.board, self.size)

        time.sleep(2)

        if self.first_turn:
            self.current_board[soldier[0][0]][soldier[0][1]] = BLANK_SPACE_CHAR
            self.current_board[soldier[1][0]][soldier[1][1]] = player_piece
            self.interface.draw_board(self.current_board)
            if opponent_player == PLAYER_B:
                self.play_state = PlayState.PLAYER_B_CHOOSING_NEUTRON
            elif opponent_player == PLAYER_A:
                self.play_state = PlayState.PLAYER_A_CHOOSING_NEUTRON
            self.interface.display_turn_information(self.play_state)
            self.interface.flip()

        else:
            self.current_board[neutron[0][0]][neutron[0][1]] = BLANK_SPACE_CHAR
            self.current_board[neutron[1][0]][neutron[1][1]] = NEUTRON_CHAR
            self.interface.draw_board(self.current_board)
            if self.current_player == PLAYER_B:
                self.play_state = PlayState.PLAYER_B_MOVING_SOLDIER
            elif self.current_player == PLAYER_A:
                self.play_state = PlayState.PLAYER_A_MOVING_SOLDIER
            self.interface.display_turn_information(self.play_state)
            self.interface.flip()

            end, winner = self.check_game_end()
            if end:
                if winner == PLAYER_B:
                    self.play_state = PlayState.PLAYER_B_WINS
                elif winner == PLAYER_A:
                    self.play_state = PlayState.PLAYER_A_WINS
            else:
                if soldier != None:
                    time.sleep(3)
                    self.current_board[soldier[0][0]][soldier[0][1]] = BLANK_SPACE_CHAR
                    self.current_board[soldier[1][0]][soldier[1][1]] = player_piece
                    self.interface.draw_board(self.current_board)
                    if self.current_player == PLAYER_B:
                        self.play_state = PlayState.PLAYER_A_MOVING_NEUTRON
                    elif self.current_player == PLAYER_A:
                        self.play_state = PlayState.PLAYER_B_MOVING_NEUTRON
                    self.interface.display_turn_information(self.play_state)
                    self.interface.flip()

                    end, winner = self.check_game_end()
                    if end:
                        if winner == PLAYER_B:
                            self.play_state = PlayState.PLAYER_B_WINS
                        elif winner == PLAYER_A:
                            self.play_state = PlayState.PLAYER_A_WINS


        self.current_player = opponent_player





    def get_neutron_piece(self):
        """
        Method that returns the coordinates of the neutron on the board.
        """
        for i in range(self.size):
            for j in range(self.size):
                if self.current_board[i][j] == NEUTRON_CHAR:
                    return j, i

    def check_game_end(self):
        """
        Method that checks if the game has ended, and if so what was the result.
        """
        neutron_square_x, neutron_square_y = self.get_neutron_piece()
        if neutron_square_y == self.size - 1:
            return True , PlayState.PLAYER_A_WINS

        elif neutron_square_y == 0:
            return True, PlayState.PLAYER_B_WINS

        else:
            possible_moves_neutron = self.possible_moves(neutron_square_x, neutron_square_y)
            if len(possible_moves_neutron) == 0:
                if self.play_state == PlayState.PLAYER_A_MOVING_SOLDIER:
                    return True, PlayState.PLAYER_A_WINS
                elif self.play_state == PlayState.PLAYER_B_MOVING_SOLDIER:
                    return True, PlayState.PLAYER_B_WINS

        return False, None


