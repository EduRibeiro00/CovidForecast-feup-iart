import pygame
import time
from .colors import Colors
from .interface_consts import BLINKING_TIME, FONT_SIZE, FONT_FILE

class Square:
    """
    Class that represents a square of the board, that may have a piece on it.
    """
    def __init__(self, x, y, color):
        """
        Constructor of the class.
        """
        self.x = x
        self.y = y
        self.color = color
        self.piece = None
        self.selected = False
        self.blinking = True
        self.before = 0
        self.delta = 0
        self.time = 0

    def set_piece(self, piece):
        """
        Method that sets the piece that is on the square.
        """
        self.piece = piece


    def get_piece(self):
        """
        Method that returns the piece that is on the square (if any).
        """
        return self.piece


    def collision(self, square_size, mouse_x, mouse_y):
        """
        Method that detects if a mouse click was inside the square.
        """
        x1 = square_size * self.x + 50
        y1 = square_size * self.y + 50
        x2 = square_size * self.x + 50 + square_size
        y2 = square_size * self.y + 50 + square_size

        if  x1 <= mouse_x <= x2 and y1 <= mouse_y <= y2:
            return True
        else:
            return False



    def draw_square(self, screen, square_size):
        """
        Method that draws on the screen the board square (and its piece if any).
        Also takes care of the blinking if the square is selected.
        """
        # draw square
        pygame.draw.rect(screen, self.color, [(square_size * self.x) + 50, (square_size * self.y) + 50, square_size, square_size])


        font = pygame.font.Font(FONT_FILE, FONT_SIZE)

        if self.x == 0 and self.y != 0:

            text = font.render(str(self.y), True, Colors.TEXT_COLOR.value, Colors.TEXT_BACKGROUND_COLOR.value)
            text_rect = text.get_rect()
            text_rect.center = (square_size * self.x + 30, square_size * self.y + 50 + square_size / 2)
            screen.blit(text, text_rect)

        elif self.y == 0 and self.x != 0:

            text = font.render(chr(65 + self.x), True, Colors.TEXT_COLOR.value, Colors.TEXT_BACKGROUND_COLOR.value)
            text_rect = text.get_rect()
            text_rect.center = (square_size * self.x + 50 + square_size / 2, square_size * self.y + 30)
            screen.blit(text, text_rect)

        elif self.y == 0 and self.x == 0:

            text = font.render(chr(65), True, Colors.TEXT_COLOR.value, Colors.TEXT_BACKGROUND_COLOR.value)
            text_rect = text.get_rect()
            text_rect.center = (square_size * self.x + 50 + square_size / 2, square_size * self.y + 30)
            screen.blit(text, text_rect)

            text = font.render(str(self.y), True, Colors.TEXT_COLOR.value, Colors.TEXT_BACKGROUND_COLOR.value)
            text_rect = text.get_rect()
            text_rect.center = (square_size * self.x + 30, square_size * self.y + 50 + square_size / 2)
            screen.blit(text, text_rect)


        # blinking if selected
        if not self.selected:
            self.before = time.time()
        elif self.selected:
            self.delta = time.time() - self.before
            self.before = time.time()
            self.time = self.time + self.delta

            if self.time > BLINKING_TIME:
                self.time = 0
                if self.blinking:
                    self.blinking = False
                else:
                   self.blinking = True

            if self.blinking:
                pygame.draw.rect(screen, Colors.SELECTED_SQUARE_COLOR.value, [(square_size * self.x) + 50, (square_size * self.y) + 50, square_size- 2, square_size- 2], 4)

        # draw piece (if any)
        if self.piece is not None:
            screen.blit(self.piece, ((square_size * self.x) + 50, (square_size * self.y) + 50))
