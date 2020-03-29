from interface.menu import *
from utils.board_utils import *
from interface.game_interface import GameInterface
from state.game_state import GameState
from state.play_state import PlayState
from ai.minimax import *
from ai.heuristic import *
import pygame
import _thread

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
        self.calculated_moves = False

        self.before = 0
        self.time_passed = 0
        self.first_cycle = True
        self.started_threading = False
        self.blinking_ai = False


    def adapt_to_board_size(self):
        """
        Method that adapts the needed parameters/variables to the selected board size.
        """
        self.size = self.menu.get_board_size()
        self.current_board = create_initial_board(self.size) # create board with the wanted size

     # -------------------
     # TODO: apagar depois de testar

    def test_minimax(self):
        self.adapt_to_board_size()

        board5 = [['B', 'B', 'B', 'B', 'B'],
                 [' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', 'N', ' ', ' '],
                 [' ', ' ', 'W', ' ', ' '],
                 ['W', 'W', ' ', 'W', 'W']]

        board7 = [['B', 'B', 'B', 'B', ' ' , 'B', 'B'],
                 [' ', ' ', ' ', 'W', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                 ['N', ' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', 'B', ' ', ' '],
                 ['W', 'W', 'W', ' ', 'W', 'W', 'W']]

        node = Node(board5, 5)
        # node = Node(board7, 7)
        node.draw_node_in_terminal()

        new_node = calculate_minimax(node, heuristic_function_medium, False, 3, PLAYER_B, PLAYER_A)

        new_node.draw_node_in_terminal()

        neutron_play, soldier_play = determine_moves_neutron_soldier(node.board, new_node.board, node.board_size)

        print(neutron_play, soldier_play)

        
     # -------------------


    def run(self):
        """
        Main method of the game class. Contains the main game cycle.
        """
        while self.game_state != GameState.EXIT:

            if self.first_cycle:
                self.first_cycle = False
                self.before = time.time()
            else:
                self.delta = time.time() - self.before
                self.before = time.time()
                self.time_passed = self.time_passed + self.delta


            if self.game_state == GameState.PLAY_PREP:
                self.adapt_to_board_size()
                self.interface.start_interface(self.size)
                self.play_state = PlayState.PLAYER_A_CHOOSING_SOLDIER
                self.game_state = GameState.PLAY
                self.first_turn = True
                self.current_player = PLAYER_A
                self.calculated_moves = False
                self.started_threading = False


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
                        self.process_events(HUMAN)


                    elif self.menu.game_mode == HUMAN_VS_COMPUTER:
                        if self.current_player == PLAYER_A:
                            self.process_events(HUMAN)
                        elif self.current_player == PLAYER_B:
                            self.process_events(COMPUTER)

                    elif self.menu.game_mode == COMPUTER_VS_HUMAN:

                        if self.current_player == PLAYER_A:
                            self.process_events(COMPUTER)
                        elif self.current_player == PLAYER_B:
                            self.process_events(HUMAN)

                    elif self.menu.game_mode == COMPUTER_VS_COMPUTER:
                        self.process_events(COMPUTER)


                else: # end play state

                    # to give time for the player to see which player has won the game
                    if self.time_passed < 4:
                        self.process_events(ENDGAME)
                    elif self.time_passed > 4:
                        self.interface.end_game()
                        self.game_state = GameState.GAME_OVER


            elif self.game_state != GameState.EXIT:
                self.game_state = self.menu.handle_menu_state(self.game_state)


    def process_events(self, current_player):
        """
        Method that processes events from the interface.
        """
        event_queue = self.interface.watch_for_events()  # get events from pygame

        if current_player == HUMAN:
            for event in event_queue:
            # quit the game
                if event == 'EVENT_QUIT':
                    self.play_state = PlayState.END
                    self.time_passed = 0

                # if the mouse button was pressed
                elif event == 'EVENT_MOUSEBUTTONDOWN':
                    self.handle_mouse_event()

        elif current_player == COMPUTER:
            for event in event_queue:
                if event == 'EVENT_QUIT':
                    self.play_state = PlayState.END
                    self.time_passed = 0

                elif event == 'EVENT_MOUSEBUTTONDOWN':
                    print("AI is still playing!")
            self.make_move_ai()

        elif current_player == ENDGAME:
            for event in event_queue:
                if event == 'EVENT_MOUSEBUTTONDOWN':
                    print("Game is ending soon!")



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
                            self.time_passed = 0
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
                            self.time_passed = 0
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
                            self.time_passed = 0
                        else:
                            self.play_state = PlayState.PLAYER_A_CHOOSING_NEUTRON
                            self.current_player = PLAYER_A
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
                            self.time_passed = 0
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

        if not self.calculated_moves and not self.started_threading:
            if self.current_player == PLAYER_B:
                self.opponent_player = PLAYER_A
                self.player_piece = PLAYER_B_SOLDIER_CHAR
            elif self.current_player == PLAYER_A:
                self.opponent_player = PLAYER_B
                self.player_piece = PLAYER_A_SOLDIER_CHAR

            _thread.start_new_thread(self.calculate_minimax_thread, ())
            self.started_threading = True


        if self.play_state == PlayState.PLAYER_A_CHOOSING_SOLDIER:

            if self.calculated_moves:
                if (self.time_passed > 3):
                    self.play_state = PlayState.PLAYER_A_MOVING_SOLDIER
                    self.interface.get_square_in_coords(self.soldier_move[0][1], self.soldier_move[0][0]).selected = False
                    self.blinking_ai = False
                elif not self.blinking_ai:
                    self.blinking_ai = True
                    self.interface.get_square_in_coords(self.soldier_move[0][1], self.soldier_move[0][0]).selected = True

        elif self.play_state == PlayState.PLAYER_A_MOVING_SOLDIER:

            self.current_board[self.soldier_move[0][0]][self.soldier_move[0][1]] = BLANK_SPACE_CHAR
            self.current_board[self.soldier_move[1][0]][self.soldier_move[1][1]] = self.player_piece

            end, winner_state = self.check_game_end()
            if end:
                self.play_state = winner_state
            else:
                self.play_state = PlayState.PLAYER_B_CHOOSING_NEUTRON

            if self.first_turn:
                self.first_turn = False

            self.current_player = self.opponent_player
            self.calculated_moves = False
            self.time_passed = 0

        elif self.play_state == PlayState.PLAYER_A_CHOOSING_NEUTRON:

            if self.calculated_moves:
                if (self.time_passed > 3):
                    self.play_state = PlayState.PLAYER_A_MOVING_SOLDIER
                    self.interface.get_square_in_coords(self.neutron_move[0][1],
                                                        self.neutron_move[0][0]).selected = False

                    self.play_state = PlayState.PLAYER_A_MOVING_NEUTRON
                    self.blinking_ai = False
                elif not self.blinking_ai:
                    self.blinking_ai = True
                    self.interface.get_square_in_coords(self.neutron_move[0][1],
                                                        self.neutron_move[0][0]).selected = True

        elif self.play_state == PlayState.PLAYER_A_MOVING_NEUTRON:

            self.current_board[self.neutron_move[0][0]][self.neutron_move[0][1]] = BLANK_SPACE_CHAR
            self.current_board[self.neutron_move[1][0]][self.neutron_move[1][1]] = NEUTRON_CHAR

            end, winner_state = self.check_game_end()
            if end:
                self.play_state = winner_state
            else:
                self.play_state = PlayState.PLAYER_A_CHOOSING_SOLDIER

            self.blinking_ai = False
            self.time_passed = 0


        elif self.play_state == PlayState.PLAYER_B_CHOOSING_SOLDIER:

            if self.calculated_moves:
                if (self.time_passed > 3):
                    self.play_state = PlayState.PLAYER_B_MOVING_SOLDIER
                    self.interface.get_square_in_coords(self.soldier_move[0][1], self.soldier_move[0][0]).selected = False
                    self.blinking_ai = False
                elif not self.blinking_ai:
                    self.blinking_ai = True
                    self.interface.get_square_in_coords(self.soldier_move[0][1], self.soldier_move[0][0]).selected = True

        elif self.play_state == PlayState.PLAYER_B_MOVING_SOLDIER:

            self.current_board[self.soldier_move[0][0]][self.soldier_move[0][1]] = BLANK_SPACE_CHAR
            self.current_board[self.soldier_move[1][0]][self.soldier_move[1][1]] = self.player_piece
            end, winner_state = self.check_game_end()
            if end:
                self.play_state = winner_state
            else:
                self.play_state = PlayState.PLAYER_A_CHOOSING_NEUTRON

            self.current_player = self.opponent_player
            self.calculated_moves = False
            self.time_passed = 0


        elif self.play_state == PlayState.PLAYER_B_CHOOSING_NEUTRON:

            if self.calculated_moves:
                if (self.time_passed > 3):
                    self.play_state = PlayState.PLAYER_A_MOVING_SOLDIER
                    self.interface.get_square_in_coords(self.neutron_move[0][1],
                                                        self.neutron_move[0][0]).selected = False
                    self.play_state = PlayState.PLAYER_B_MOVING_NEUTRON
                    self.blinking_ai = False
                elif not self.blinking_ai:
                    self.blinking_ai = True
                    self.interface.get_square_in_coords(self.neutron_move[0][1],
                                                        self.neutron_move[0][0]).selected = True


        elif self.play_state == PlayState.PLAYER_B_MOVING_NEUTRON:

            self.current_board[self.neutron_move[0][0]][self.neutron_move[0][1]] = BLANK_SPACE_CHAR
            self.current_board[self.neutron_move[1][0]][self.neutron_move[1][1]] = NEUTRON_CHAR

            end, winner_state = self.check_game_end()
            if end:
                self.play_state = winner_state
            else:
                self.play_state = PlayState.PLAYER_B_CHOOSING_SOLDIER

            self.time_passed = 0



    def calculate_minimax_thread(self):
        """
        Function
        """
        if self.current_player == PLAYER_A:
            evaluator = self.menu.evaluator_a
            max_depth = self.menu.max_depth_a
        else:
            evaluator = self.menu.evaluator_b
            max_depth = self.menu.max_depth_b

        node = Node(self.current_board, self.size)
        new_node = calculate_minimax(node, evaluator, self.first_turn, max_depth, self.current_player, self.opponent_player)
        self.neutron_move, self.soldier_move = determine_moves_neutron_soldier(self.current_board, new_node.board, self.size)
        self.calculated_moves = True
        self.time_passed = 0
        self.started_threading = False


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


