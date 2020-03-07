import pygame
import os
from .colors import Colors
from .square import Square

# screen and board dimensions
SQUARE_SIZE = 70

class GameInterface:
    """
    Class representing the interface (interface + controller) of the game.
    """
    def __init__(self, board_size):
        """
        Constructor of the class.
        """
        pygame.init()
        self.board_size = board_size
        self.screen_width = SQUARE_SIZE * self.board_size + 200
        self.screen_height = SQUARE_SIZE * self.board_size + 100
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])
        pygame.display.set_caption("Neutron")

        self.load_img_resources()
        self.init_board_squares()


    def init_board_squares(self):
        """
        Method that constructs and initializes the board squares.
        """
        self.squares = []

        cnt = 0
        for row_num in range(self.board_size):
            for col_num in range(self.board_size):
                if cnt % 2 == 0:
                    color = Colors.SQUARE_COLOR_1.value
                else:
                    color = Colors.SQUARE_COLOR_2.value

                self.squares.append(Square(row_num, col_num, color))
                cnt += 1


    def load_img_resources(self):
        """
        Methods that loads and saves the sprites for the game.
        """
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.black_soldier_img = pygame.image.load(current_dir + "/../../res/pawn_black.png")
        self.white_soldier_img = pygame.image.load(current_dir + "/../../res/pawn_white.png")
        self.neutron_img = pygame.image.load(current_dir + "/../../res/neutron.png")
        # TODO: bolinha verde para indicar que a casa e valida para se fazer um move quando o humano clica numa peça


    def get_square_in_coords(self, x, y):
        """
        Method that, given the x-y coordinates of a board position, returns its square.
        """
        pos = (x * self.board_size) + y
        if pos >= len(self.squares):
            return None

        return self.squares[pos]


    def update_interface_board(self, board):
        """
        Method that receives the board and updates the squares with their pieces.
        """
        for x in range(self.board_size):
            for y in range(self.board_size):
                board_cell = board[x][y]
                board_square = self.get_square_in_coords(x, y)
                if board_cell == 'W':
                    board_square.set_piece(self.white_soldier_img)
                elif board_cell == 'B':
                    board_square.set_piece(self.black_soldier_img)
                elif board_cell == 'N':
                    board_square.set_piece(self.neutron_img)
                elif board_cell == ' ':
                    board_square.set_piece(None)


    def watch_for_events(self):
        """
        Returns list with all pygame detected events in the current instant.
        """
        event_queue = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                event_queue.append('EVENT_QUIT')
            # TODO: ver os outros eventos

        return event_queue


    def draw_board(self, board):
        """
        Method to draw a node and its board on the pygame interface.
        """
        self.update_interface_board(board)
        self.screen.fill(Colors.BACKGROUND_COLOR.value)  # fill the screen with black

        # draw all squares
        for square in self.squares:
            square.draw_square(self.screen, SQUARE_SIZE)

        # Add a nice border
        pygame.draw.rect(self.screen, Colors.BOARD_BORDER_COLOR.value, [40, 50, self.board_size * SQUARE_SIZE, self.board_size * SQUARE_SIZE], 4)

        pygame.display.flip()


    def exit(self):
        """
        Method to exit.
        """
        pygame.quit()
