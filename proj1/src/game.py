from utils.board_utils import *
from interface.game_interface import GameInterface
from state.game_state import GameState
from state.play_state import PlayState
import pygame

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

            # TODO: processar os outros eventos


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
                        self.selected_piece_x = x
                        self.selected_piece_y = y
                        self.play_state = PlayState.PLAYER_A_MOVING_SOLDIER

                elif self.play_state == PlayState.PLAYER_A_MOVING_SOLDIER:
                    if self.current_board[y][x] == BLANK_SPACE_CHAR:
                        self.current_board[self.selected_piece_y][self.selected_piece_x] = BLANK_SPACE_CHAR
                        self.current_board[y][x] = PLAYER_A_SOLDIER_CHAR
                        # put the condition in case it is the first play of the game
                        self.play_state = PlayState.PLAYER_A_CHOOSING_NEUTRON

                elif self.play_state == PlayState.PLAYER_A_CHOOSING_NEUTRON:
                    if self.current_board[y][x] == NEUTRON_CHAR:
                        self.selected_piece_x = x
                        self.selected_piece_y = y
                        self.play_state = PlayState.PLAYER_A_MOVING_NEUTRON

                elif self.play_state == PlayState.PLAYER_A_MOVING_NEUTRON:
                    if self.current_board[y][x] == BLANK_SPACE_CHAR:
                        self.current_board[self.selected_piece_y][self.selected_piece_x] = BLANK_SPACE_CHAR
                        self.current_board[y][x] = NEUTRON_CHAR
                        self.play_state = PlayState.PLAYER_B_CHOOSING_SOLDIER

                elif self.play_state == PlayState.PLAYER_B_CHOOSING_SOLDIER:
                    if self.current_board[y][x] == PLAYER_B_SOLDIER_CHAR:
                        self.selected_piece_x = x
                        self.selected_piece_y = y
                        self.play_state = PlayState.PLAYER_B_MOVING_SOLDIER

                elif self.play_state == PlayState.PLAYER_B_MOVING_SOLDIER:
                    if self.current_board[y][x] == BLANK_SPACE_CHAR:
                        self.current_board[self.selected_piece_y][self.selected_piece_x] = BLANK_SPACE_CHAR
                        self.current_board[y][x] = PLAYER_B_SOLDIER_CHAR
                        self.play_state = PlayState.PLAYER_B_MOVING_NEUTRON

                elif self.play_state == PlayState.PLAYER_B_MOVING_NEUTRON:
                    if self.current_board[y][x] == NEUTRON_CHAR:
                        self.selected_piece_x = x
                        self.selected_piece_y = y
                        self.play_state = PlayState.PLAYER_B_CHOOSING_NEUTRON

                elif self.play_state == PlayState.PLAYER_B_CHOOSING_NEUTRON:
                    if self.current_board[y][x] == BLANK_SPACE_CHAR:
                        self.current_board[self.selected_piece_y][self.selected_piece_x] = BLANK_SPACE_CHAR
                        self.current_board[y][x] = NEUTRON_CHAR
                        self.play_state = PlayState.PLAYER_A_CHOOSING_SOLDIER



    def possible_moves(self, x, y):
        """
        Method that calculates all possible movements of a given piece
        """
        possibilities = []
        
        if x != self.size - 1:
            for i in range(1, self.size - x):
                if (i != 1 and self.current_board[y][x+i] != BLANK_SPACE_CHAR) or x + i == self.size - 1:
                    coords = (x + i - 1, y)
                    possibilities.append(coords)
                    break

        if x != 0:
            for i in range(1, x + 1):
                if (i != 1 and self.current_board[y][x-i] != BLANK_SPACE_CHAR) or x - i == 0:
                    coords = (x - i, y)
                    possibilities.append(coords)
                    break

        if y != self.size - 1:
            for i in range(1, self.size - y):
                if (i != 1 and self.current_board[y+i][x] != BLANK_SPACE_CHAR) or y + i == self.size - 1:
                    coords = (x, y + i - 1)
                    possibilities.append(coords)
                    break

        if y != 0:
            for i in range(1, y + 1):
                if (i != 1 and self.current_board[y- i][x] != BLANK_SPACE_CHAR) or y - i == 0:
                    coords = (x, y - i)
                    possibilities.append(coords)
                    break 

        if x != self.size - 1 and y != self.size - 1:
            limit = min([self.size - x, self.size - y])
            for i in range(1, limit):
                if (i != 1 and self.current_board[y+i][x+i] != BLANK_SPACE_CHAR) or x + i == self.size - 1 or y + i == self.size - 1:
                    coords = (x + i, y + i)
                    possibilities.append(coords)
                    break    

        if x != self.size - 1 and y != 0:
            limit = min([self.size - x, y + 1])
            for i in range(1, limit):
                if (i != 1 and self.current_board[y-i][x+i] != BLANK_SPACE_CHAR) or x + i == self.size - 1 or y - i == 0:
                    coords = (x + i, y - i)
                    possibilities.append(coords)
                    break  

        if x != 0 and y != 0:
            limit = min([x + 1, y + 1])
            for i in range(1, limit):
                if (i != 1 and self.current_board[y-i][x-i] != BLANK_SPACE_CHAR) or x - i == 0 or y - i == 0:
                    coords = (x - i, y - i)
                    possibilities.append(coords)
                    break    

        if x != 0 and y != self.size - 1:
            limit = min([x + 1, self.size - y])
            for i in range(1, limit):
                if (i != 1 and self.current_board[y+i][x-i] != BLANK_SPACE_CHAR) or x - i == 0 or y + i == self.size - 1:
                    coords = (x - i, y + i)
                    possibilities.append(coords)
                    break                                                                     
                


    def exit(self):
        """
        Method to exit.
        """
        self.interface.exit()