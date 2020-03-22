from random import randrange

def read_from_file(filename):
    """
    Function that reads from file and returns the
    data in it.
    """
    f = open(filename)
    lines = f.readlines()

    [num_slots, num_subjects] = lines[0].split()
    num_slots = int(num_slots)
    num_subjects = int(num_subjects)
    lines.pop(0)

    list_registered = []
    for line in lines:
        list_registered.append(line.split())

    return num_slots, num_subjects, list_registered



def calc_incompatibilities(list_registered):
    """
    Returns a dict with key "subjectnum1_subjectnum2" and value equal to the number of
    incompatibilities.
    """
    incompatibilities_dict = {}

    for i, subj_students in enumerate(list_registered):
        for j in range(i + 1, len(list_registered)):

            other_subj_students = list_registered[j]
            incompatibilities = 0

            for student in subj_students:
                if student in other_subj_students:
                    incompatibilities += 1

            key = str(i) + "_" + str(j)
            incompatibilities_dict[key] = incompatibilities

    return incompatibilities_dict


def gen_random_allocation(num_slots, num_subjects):
    """
    Given the number of slots and the number of subjects, returns
    a state with a random student allocation.
    """
    subj_slots = []
    for i in range(num_subjects):
        subj_slots.append(randrange(num_slots) + 1)

    return subj_slots