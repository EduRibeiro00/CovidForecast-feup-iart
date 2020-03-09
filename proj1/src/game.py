from ai.node import Node
from utils.board_utils import create_initial_board
from interface.game_interface import GameInterface
from state.game_state import GameState
from state.play_state import PlayState
from interface.colors import Colors
import pygame, sys


class Game:
    """
    Main class representing the game.
    """
    def __init__(self, size):
        """
        Constructor of the class.
        """
        self.current_player = 'white' # white player starts first
        self.current_board = create_initial_board(size) # create board with the wanted size
        self.interface = GameInterface(size)
        self.game_state = GameState.PLAY
        self.play_state = PlayState.PLAYER_A_CHOOSING_SOLDIER
        self.player_A_soldier = 'W'
        self.player_B_soldier = 'B'
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
            if event == 'EVENT_QUIT': # quit the game
                self.game_state = GameState.EXIT
            elif event == 'EVENT_MOUSEBUTTONDOWN':
                if self.game_state == GameState.PLAY:
                    # mouse coordinates
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    square = self.interface.check_collision(mouse_x, mouse_y)

                    if square is not None:

                        # represents the columns
                        x = square.x
                        # represents the rows
                        y = square.y
                        if self.play_state == PlayState.PLAYER_A_CHOOSING_SOLDIER:
                            if self.current_board[y][x] == self.player_A_soldier:
                                self.selected_piece_x = x
                                self.selected_piece_y = y
                                self.play_state = PlayState.PLAYER_A_MOVING_SOLDIER

                        elif self.play_state == PlayState.PLAYER_A_MOVING_SOLDIER:
                            if self.current_board[y][x] == ' ':
                                self.current_board[self.selected_piece_y][self.selected_piece_x] = " "
                                self.current_board[y][x] = self.player_A_soldier
                                # put the condition in case it is the first play of the game
                                self.play_state = PlayState.PLAYER_A_CHOOSING_NEUTRON

                        elif self.play_state == PlayState.PLAYER_A_CHOOSING_NEUTRON:
                            if self.current_board[y][x] == 'N':
                                self.selected_piece_x = x
                                self.selected_piece_y = y
                                self.play_state = PlayState.PLAYER_A_MOVING_NEUTRON

                        elif self.play_state == PlayState.PLAYER_A_MOVING_NEUTRON:
                            if self.current_board[y][x] == " ":
                                self.current_board[self.selected_piece_y][self.selected_piece_x] = " "
                                self.current_board[y][x] = 'N'
                                self.play_state = PlayState.PLAYER_B_CHOOSING_SOLDIER

                        elif self.play_state == PlayState.PLAYER_B_CHOOSING_SOLDIER:
                            if self.current_board[y][x] == self.player_B_soldier:
                                self.selected_piece_x = x
                                self.selected_piece_y = y
                                self.play_state = PlayState.PLAYER_B_MOVING_SOLDIER

                        elif self.play_state == PlayState.PLAYER_B_MOVING_SOLDIER:
                            if self.current_board[y][x] == ' ':
                                self.current_board[self.selected_piece_y][self.selected_piece_x] = " "
                                self.current_board[y][x] = self.player_B_soldier
                                self.play_state = PlayState.PLAYER_B_MOVING_NEUTRON

                        elif self.play_state == PlayState.PLAYER_B_MOVING_NEUTRON:
                            if self.current_board[y][x] == 'N':
                                self.selected_piece_x = x
                                self.selected_piece_y = y
                                self.play_state = PlayState.PLAYER_B_CHOOSING_NEUTRON

                        elif self.play_state == PlayState.PLAYER_B_CHOOSING_NEUTRON:
                            if self.current_board[y][x] == " ":
                                self.current_board[self.selected_piece_y][self.selected_piece_x] = " "
                                self.current_board[y][x] = 'N'
                                self.play_state = PlayState.PLAYER_A_CHOOSING_SOLDIER





            # TODO: processar os outros eventos




    def exit(self):
        """
        Method to exit.
        """
        self.interface.exit()