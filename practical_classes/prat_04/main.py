from prat_04.algs import hill_climbing, steepest_ascent_hill_climbing, simulated_annealing
from prat_04.state import State
from prat_04.utils import read_from_file, gen_random_allocation, calc_incompatibilities

if __name__ == '__main__':
    num_slots, num_subjects, list_registered = read_from_file('info.txt')
    incompatibilities = calc_incompatibilities(list_registered)
    MAX_NUM_ITERS = 500
    ANNEALING_STEP = 0.0025

    # state = State(incompatibilities, gen_random_allocation(num_slots, num_subjects))
    # state = State(incompatibilities, [1,1,1,1,1,1,1,1,1,1,1,1])
    # state = State(incompatibilities, [1,1,1,2,2,2,3,3,3,4,4,1])
    # state = State(incompatibilities, [1,1,4,2,2,2,3,3,3,4,4,1])
    state = State(incompatibilities, [1,2,3,4,1,2,3,4,1,2,3,4])

    new_state = hill_climbing(state, incompatibilities, num_slots, MAX_NUM_ITERS)
    # new_state = steepest_ascent_hill_climbing(state, incompatibilities, num_slots, MAX_NUM_ITERS)
    # new_state = simulated_annealing(state, incompatibilities, num_slots, ANNEALING_STEP)

    print("Final state: {state}".format(state=new_state))



