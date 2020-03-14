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
        self.screen_width = SQUARE_SIZE * self.board_size + 250
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

                self.squares.append(Square(col_num, row_num, color))
                cnt += 1



    def load_img_resources(self):
        """
        Methods that loads and saves the sprites for the game, and calculates attributes related to those sprites
        """
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.black_soldier_img = pygame.image.load(current_dir + "/../../res/pawn_black.png")
        self.white_soldier_img = pygame.image.load(current_dir + "/../../res/pawn_white.png")
        self.neutron_img = pygame.image.load(current_dir + "/../../res/neutron.png")
        self.green_ball_img = pygame.image.load(current_dir + "/../../res/green_ball.png")

        self.soldier_width, self.soldier_height = self.black_soldier_img.get_rect().size


    def get_square_in_coords(self, x, y):
        """
        Method that, given the x-y coordinates of a board position, returns its square.
        """
        pos = (y * self.board_size) + x
        if pos >= len(self.squares):
            return None

        return self.squares[pos]


    def update_interface_board(self, board):
        """
        Method that receives the board and updates the squares with their pieces.
        """
        for y in range(self.board_size):
            for x in range(self.board_size):
                board_cell = board[y][x]
                board_square = self.get_square_in_coords(x, y)
                if board_cell == 'W':
                    board_square.set_piece(self.white_soldier_img)
                elif board_cell == 'B':
                    board_square.set_piece(self.black_soldier_img)
                elif board_cell == 'N':
                    board_square.set_piece(self.neutron_img)
                elif board_cell == ' ' and board_square.piece != self.green_ball_img:
                    board_square.set_piece(None)


    def watch_for_events(self):
        """
        Returns list with all pygame detected events in the current instant.
        """
        event_queue = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                event_queue.append('EVENT_QUIT')
            if event.type == pygame.MOUSEBUTTONDOWN:
                event_queue.append('EVENT_MOUSEBUTTONDOWN')

        return event_queue


    def draw_board(self, board):
        """
        Method to draw a node and its board on the pygame interface.
        """
        self.update_interface_board(board)
        self.screen.fill(Colors.BACKGROUND_COLOR.value)  # fill the screen with black

        # Add a nice border
        # It should be pygame.draw.rect(self.screen, Colors.BOARD_BORDER_COLOR.value, [46, 46, self.board_size * SQUARE_SIZE + 4, self.board_size * SQUARE_SIZE + 4], 4)
        # but for some reason when displaying it appears wrong
        pygame.draw.rect(self.screen, Colors.BOARD_BORDER_COLOR.value, [46, 47, self.board_size * SQUARE_SIZE + 5.9, self.board_size * SQUARE_SIZE + 5.8], 4)

        # draw all squares
        for square in self.squares:
            square.draw_square(self.screen, SQUARE_SIZE)



    def check_collision(self):
        """
        Method to check if a player has clicked the mouse and selected any of the squares.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for square in self.squares:
            if square.collision(SQUARE_SIZE, mouse_x, mouse_y):
                return square

        return None


    def highlight_squares(self, coords):
        """
        Method that allows square highlighting for possible moves.
        """
        for coord in coords:
            x, y = coord
            board_square = self.get_square_in_coords(x, y)
            board_square.set_piece(self.green_ball_img)


    def reset_highlight(self):
        """
        Method that removes highlighting from squares.
        """
        for square in self.squares:
            if square.piece == self.green_ball_img:
                square.piece = None


    def set_selected_square(self, x, y):
        """
        Method that make a selected square start to blink if it has a piece.
        """
        self.get_square_in_coords(x, y).selected = True


    def unset_selected_square(self, x, y):
        """
        Method that make a selected square stop to blink if it has a piece.
        """
        self.get_square_in_coords(x, y).selected = False


    def display_turn_information(self):
        """
        Method that displays the turn information, indicating the who has the active turn and
        which type of piece they should move.
        """
        green = (0, 255, 0)
        blue = (0, 0, 128)

        # create a font object.
        # 1st parameter is the font file
        # which is present in pygame.
        # 2nd parameter is size of the font
        font = pygame.font.Font('freesansbold.ttf', 17)

        # create a text suface object,
        # on which text is drawn on it.
        current_player_text = font.render('Current player', True, green, blue)

        move_piece_text = font.render('Move piece', True, green, blue)

        # create a rectangular object for the
        # text surface object
        current_player_textRect = current_player_text.get_rect()

        move_piece_textRect = current_player_text.get_rect()

        # set the center of the rectangular object.
        current_player_textRect.center = (self.screen_width - 100 , self.screen_height // 3)



        self.screen.blit(current_player_text, current_player_textRect)

        self.screen.blit(self.black_soldier_img, (self.screen_width - 100 - 50, self.screen_height // 3 + 15))

        move_piece_textRect.center = (self.screen_width - 100 , self.screen_height // 3 + self.soldier_height + 50)

        self.screen.blit(self.neutron_img, (self.screen_width - 100 - 50, self.screen_height // 3 + self.soldier_height * 2 ))

        self.screen.blit(move_piece_text, move_piece_textRect)


    def flip(self):
        """
        Wrapper function to flip the screen.
        """
        pygame.display.flip()


    def exit(self):
        """
        Method to exit.
        """
        pygame.quit()


