from prat_05.gen import calc_solution_genetic_alg
from prat_05.utils import read_from_file, calc_incompatibilities

if __name__ == '__main__':
    num_slots, num_subjects, list_registered = read_from_file('info.txt')
    incompatibilities = calc_incompatibilities(list_registered)
    NUM_GENERATIONS = 100
    POPULATION_SIZE = 50


    best_state = calc_solution_genetic_alg(incompatibilities, num_slots, num_subjects, NUM_GENERATIONS, POPULATION_SIZE)