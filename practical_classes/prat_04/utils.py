from prat_04.state import State

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

    return State(num_slots, num_subjects, list_registered)

