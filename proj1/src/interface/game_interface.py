import pygame
from .colors import Colors

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
        self.board_size = board_size
        self.square_size = 70

        self.screen_width = self.square_size * self.board_size + 200
        self.screen_height = self.square_size * self.board_size + 100

        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])
        pygame.display.set_caption("Neutron")
        # TODO: fazer depender o tamanho do ecra do board size


    def draw_background(self):
        """
        Method that allows to draw the checkered background board onto the screen.
        """
        self.screen.fill(Colors.BACKGROUND_COLOR.value) # fill the screen with black

        cnt = 0
        for i in range(self.board_size):
            for z in range(self.board_size):
                # check if current loop value is even
                if cnt % 2 == 0:
                    pygame.draw.rect(self.screen, Colors.SQUARE_COLOR_1.value, [(self.square_size * z) + 40, (self.square_size * i) + 50, self.square_size, self.square_size])
                else:
                    pygame.draw.rect(self.screen, Colors.SQUARE_COLOR_2.value, [(self.square_size * z) + 40, (self.square_size * i) + 50, self.square_size, self.square_size])
                cnt += 1

        # Add a nice boarder
        pygame.draw.rect(self.screen, Colors.BOARD_BORDER_COLOR.value, [40, 50, self.board_size * self.square_size, self.board_size * self.square_size], 1)
        pygame.display.flip()



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