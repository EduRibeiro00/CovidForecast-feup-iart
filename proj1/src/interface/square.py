class Square:
    """
    Class that represents a square of the board, that may have a piece on it.
    """
    def __init__(self, x, y, piece=None):
        """
        Constructor of the class.
        """
        self.x = x
        self.y = y
        self.piece = piece

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