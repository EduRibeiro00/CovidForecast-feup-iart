class State:
    """
    Class representing the state.
    """
    def __init__(self, cap_a, cap_b):
        """
        Constructor of the class.
        :param cap_a: Capacity of bucket a
        :param cap_b: Capacity of bucket b
        """
        self.cap_a = cap_a
        self.cap_b = cap_b
        self.parent = None
        self.depth = 0

    def set_parent(self, state):
        self.parent = state
        self.depth = state.depth + 1

    def is_final_state(self):
        """
        Check if the state is final.
        :return: True or False
        """
        return self.cap_a == 2 and self.cap_b == 0


    def empty_first(self, states):
        if self.cap_a == 0:
            return None

        new_state = State(0, self.cap_b)

        for other_state in states:
            if new_state == other_state:
                return None

        return new_state

    def empty_second(self, states):
        if self.cap_b == 0:
            return None

        new_state = State(self.cap_a, 0)

        for other_state in states:
            if new_state == other_state:
                return None

        return new_state

    def fill_first(self, states):
        if self.cap_a == 4:
            return None

        new_state = State(4, self.cap_b)

        for other_state in states:
            if new_state == other_state:
                return None

        return new_state

    def fill_second(self, states):
        if self.cap_b == 3:
            return None

        new_state = State(self.cap_a, 3)

        for other_state in states:
            if new_state == other_state:
                return None

        return new_state

    def transf_12_empty(self, states):
        if self.cap_a + self.cap_b > 3 or self.cap_a == 0:
            return None

        new_state = State(0, self.cap_a + self.cap_b)

        for other_state in states:
            if new_state == other_state:
                return None

        return new_state

    def transf_12_full(self, states):
        if self.cap_a + self.cap_b <= 3 or self.cap_b == 3:
            return None

        new_state = State(self.cap_a - (3 - self.cap_b), 3)

        for other_state in states:
            if new_state == other_state:
                return None

        return new_state

    def transf_21_empty(self, states):
        if self.cap_a + self.cap_b > 4 or self.cap_b == 0:
            return None

        new_state = State(self.cap_a + self.cap_b, 0)

        for other_state in states:
            if new_state == other_state:
                return None

        return new_state

    def transf_21_full(self, states):
        if self.cap_a + self.cap_b <= 4 or self.cap_a == 4:
            return None

        new_state = State(4, self.cap_b - (4 - self.cap_a))

        for other_state in states:
            if new_state == other_state:
                return None

        return new_state

    def __str__(self):
        string = self.str_only_value() + " -> " + str(self.depth)
        if self.parent:
            string += " -> " + self.parent.str_only_value()

        return string

    def str_only_value(self):
        return "[" + str(self.cap_a) + " ; " + str(self.cap_b) + "]"

    def __eq__(self, other):
        return self.cap_a == other.cap_a and self.cap_b == other.cap_b