from utils.board_utils import *
from interface.game_interface import GameInterface
from state.game_state import GameState
from state.play_state import PlayState


class Game:
    """
    Main class representing the game.
    """
    def __init__(self, size):
        """
        Constructor of the class.
        """
        self.current_board = create_initial_board(size) # create board with the wanted size
        self.size = size
        self.interface = GameInterface(size)
        self.game_state = GameState.PLAY
        self.play_state = PlayState.PLAYER_A_CHOOSING_SOLDIER
        self.selected_piece_x = None
        self.selected_piece_y = None


    def run(self):
        """
        Main method of the game class. Contains the main game cycle.
        """
        while self.game_state != GameState.EXIT:
            self.process_events()

            self.interface.draw_board(self.current_board)
            self.interface.display_turn_information(self.play_state)

            self.interface.flip()


    def process_events(self):
        """
        Method that processes events from the interface.
        """
        event_queue = self.interface.watch_for_events()  # get events from pygame

        for event in event_queue:
            # quit the game
            if event == 'EVENT_QUIT':
                self.game_state = GameState.EXIT

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


    def get_neutron_piece(self):
        """
        Method that returns the coordinates of the neutron on the board.
        """
        for i in range(self.size):
            for j in range(self.size):
                if self.current_board[i][j] == NEUTRON_CHAR:
                    return j, i


    def does_player_a_win(self, neutron_square_y):
        """
        Method that checks if player A has won.
        """
        if neutron_square_y == 0:
            return True
        return False


    def does_player_b_win(self, neutron_square_y):
        """
        Method that checks if player B has won.
        """
        if neutron_square_y == self.size - 1:
            return True
        return False


    def check_game_end(self):
        """
        Method that checks if the game has ended, and if so what was the result.
        """
        neutron_square_x, neutron_square_y = self.get_neutron_piece()
        if self.does_player_a_win(neutron_square_y):
            return True , PlayState.PLAYER_A_WINS

        elif self.does_player_b_win(neutron_square_y):
            return True, PlayState.PLAYER_B_WINS

        else:
            possible_moves_neutron = self.possible_moves(neutron_square_x, neutron_square_y)
            if len(possible_moves_neutron) == 0:
                return True, PlayState.DRAW
            # TODO: esta mal, se o neutron estiver rodeado o jogador que jogaria a seguir perde

        return False, None


    def exit(self):
        """
        Method to exit.
        """
        self.interface.exit()