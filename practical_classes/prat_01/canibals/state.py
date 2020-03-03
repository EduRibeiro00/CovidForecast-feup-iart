class State:
    """
    Class representing the state.
    """
    def __init__(self, cannibals, missionaries, boat):
        """
        Constructor of state.
        :param cannibals: Number of cannibals in the left side.
        :param missionaries:  Number of missionaries in the left side.
        :param boat: Flag that indicates if the boat is in the left side or not
        """
        self.cannibals = cannibals
        self.missionaries = missionaries
        self.boat = boat
        self.parent = None
        self.depth = 0


    def set_parent(self, state):
        self.parent = state
        self.depth = state.depth + 1


    def is_valid_state(self):
        """
        Verifies if the number of cannibals is lower or equal to the
        number of missionaries in each margin.
        """
        missionaries_left = self.missionaries
        missionaries_right = 3 - self.missionaries
        cannibals_left = self.cannibals
        cannibals_right = 3 - self.cannibals

        left_ok = (missionaries_left >= cannibals_left or missionaries_left == 0)
        right_ok = (missionaries_right >= cannibals_right or missionaries_right == 0)

        return left_ok and right_ok


    def is_final_state(self):
        """
        Check if the state is final.
        :return: True or False
        """
        return self.cannibals == 0 and self.missionaries == 0

    def __str__(self):
        string = self.str_only_value() + " -> " + str(self.depth)
        if self.parent:
            string += " -> " + self.parent.str_only_value()

        return string

    def str_only_value(self):
        return "[" + str(self.cannibals) + " ; " + str(self.missionaries) + " ; " + str(self.boat) + "]"

    def __eq__(self, other):
        return self.cannibals == other.cannibals and self.missionaries == other.missionaries and self.boat == other.boat