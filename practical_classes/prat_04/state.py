class State:
    def __init__(self, incompatibilies, subj_slots):
        """
        Constructor of the class.
        """
        self.subj_slots = subj_slots # list where index is subject and value is subject's slot
        self.score = self.calc_solution_score(incompatibilies)


    def get_score(self):
        """
        Method that retrieves the state's score.
        """
        return self.score


    def calc_solution_score(self, incompatibilities):
        """
        Calculate the score of the state's solution to the problem.
        The lower the score the better, because the score shows the
        total number of students in incompatible classes.
        """
        score = 0

        for i, class_slot_1 in enumerate(self.subj_slots):
            for j in range(i + 1, len(self.subj_slots)):
                class_slot_2 = self.subj_slots[j]

                if class_slot_1 == class_slot_2: # if they are on the same slot
                    key = str(i) + "_" + str(j)
                    num_students = incompatibilities[key]
                    score += num_students

        return score


    def generate_neighbours(self, incompatibilities, num_slots):
        """
        Generator function that returns neighbours of the current state.
        """
        slots_list = [i + 1 for i in range(num_slots)]

        for idx, subject_slot in enumerate(self.subj_slots):
            new_subj_slots = list(self.subj_slots)
            slots_list_aux = list(slots_list)
            slots_list_aux.remove(subject_slot)
            for other_slots in slots_list_aux:
                new_subj_slots[idx] = other_slots
                yield State(incompatibilities, new_subj_slots)


    def __str__(self):
        """
        Overload of the to-string operator.
        """
        return "{slots} ; score = {score}".format(slots=self.subj_slots, score=self.score)




