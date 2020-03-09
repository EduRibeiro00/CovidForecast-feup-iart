from ai.node import Node
from utils.board_utils import create_initial_board
from interface.game_interface import GameInterface
from state.game_state import GameState
from state.play_state import PlayState
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
                    #mouse coordinates

                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.interface.check_collision(mouse_x, mouse_y)






            # TODO: processar os outros eventos




    def exit(self):
        """
        Method to exit.
        """
        self.interface.exit()