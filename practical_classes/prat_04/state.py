class State:
    def __init__(self, num_slots, num_subjects, list_registered, subj_slots):
        """
        Constructor of the class.
        """
        self.num_slots = num_slots
        self.num_subjects = num_subjects
        self.list_registered = list_registered
        self.incompatibilities = {}
        self.calc_incompatibilities()
        self.subj_slots = subj_slots # list where index is subject and value is subject's slot

    def get_num_slots(self):
        return self.num_slots

    def get_num_subjects(self):
        return self.num_subjects

    def get_list_registered(self):
        return self.list_registered

    def get_incompatibilities(self):
        return self.incompatibilities

    def calc_incompatibilities(self):
        """
        Returns a dict with key "subjectnum1_subjectnum2" and value equal to the number of
        incompatibilities.
        """
        for i, subj_students in enumerate(self.list_registered):
            for j in range(i + 1, len(self.list_registered)):

                other_subj_students = self.list_registered[j]
                incompatibilities = 0

                for student in subj_students:
                    if student in other_subj_students:
                        incompatibilities += 1

                key = str(i) + "_" + str(j)
                self.incompatibilities[key] = incompatibilities


    def calc_solution_score(self):
        """
        Calculate the score of the state's solution to the problem,
        """
