import pygame

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

        x1 = square_size * self.x + 40
        y1 = square_size * self.y + 50
        x2 = square_size * self.x + 40 + square_size
        y2 = square_size * self.y + 50 + square_size

        if  x1 <= mouse_x <= x2 and y1 <= mouse_y <= y2:
            print("Tocou na peça " + "(" + str(self.x) + "," + str(self.y) + ")")
            return True
        else:
            return False




    def draw_square(self, screen, square_size):
        """
        Method that draws on the screen the board square (and its piece if any)
        """
        pygame.draw.rect(screen, self.color, [(square_size * self.x) + 40, (square_size * self.y) + 50, square_size, square_size])

        if self.piece is not None:
            screen.blit(self.piece, ((square_size * self.x) + 40, (square_size * self.y) + 50))