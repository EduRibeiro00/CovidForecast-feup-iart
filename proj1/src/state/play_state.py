import enum

class PlayState(enum.Enum):
    """
    Class representing the states for when a game is underway.
    """
    PLAYER_A_CHOOSING_SOLDIER = 1
    PLAYER_A_MOVING_SOLDIER = 2
    PLAYER_A_CHOOSING_NEUTRON = 3
    PLAYER_A_MOVING_NEUTRON = 4
    PLAYER_B_CHOOSING_SOLDIER = 5
    PLAYER_B_MOVING_SOLDIER = 6
    PLAYER_B_CHOOSING_NEUTRON = 7
    PLAYER_B_MOVING_NEUTRON = 8
    PLAYER_A_WINS = 9
    PLAYER_B_WINS = 10
    DRAW = 11

