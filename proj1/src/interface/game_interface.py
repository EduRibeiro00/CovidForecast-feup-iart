import pygame


# screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

class GameInterface:
    """
    Class representing the interface (interface + controller) of the game.
    """
    def __init__(self, board_size):
        """
        Constructor of the class.
        """
        pygame.init()
        pygame.display.set_caption("Neutron")
        self.board_size = board_size
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        # TODO: fazer depender o tamanho do ecra do board size


    def draw_background(self):
        """
        Method that allows to draw the checkered background board onto the screen.
        """
        self.screen.fill((0, 0, 0)) # fill the screen with black

        screen_size = SCREEN_HEIGHT if SCREEN_WIDTH > SCREEN_HEIGHT else SCREEN_WIDTH
        square_size = screen_size / self.board_size

        cnt = 0
        for i in range(1, self.screen + 1):
            for z in range(1, self.screen + 1):
                # check if current loop value is even
                if cnt % 2 == 0:
                    pygame.draw.rect(self.screen, (163, 108, 78), [square_size * z, square_size * i, square_size, square_size])
                else:
                    pygame.draw.rect(self.screen, (0, 0, 0), [square_size * z, square_size * i, square_size, square_size])
                cnt += 1

        # Add a nice boarder
        pygame.draw.rect(self.screen, (128, 123, 120), [square_size, square_size, self.board_size * square_size, self.board_size * square_size], 1)



    def draw_node(self):
        """
        Method to draw a node and its board on the pygame interface.
        """
        # TODO: draw board


    def exit(self):
        """
        Method to exit.
        """
        pygame.quit()