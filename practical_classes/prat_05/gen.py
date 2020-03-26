import random
from copy import copy
from prat_05.state import State
from prat_05.utils import gen_random_allocation

def selection_with_tournament(slots_list, percentage):
    # number of tournaments will be equal to the number of individuals to pass through
    num_tournaments = int(len(slots_list) * percentage)

    # number of participants per tournament (some individuals can be left off)
    num_participants = len(slots_list) // num_tournaments

    champions = []
    for _ in range(num_tournaments):
        tournament_winner = None
        for _ in range(num_participants):
            participant = random.choice(slots_list)
            slots_list.remove(participant)

            if tournament_winner is None or tournament_winner.get_fitness() > participant.get_fitness():
                tournament_winner = participant

        if tournament_winner is not None:
            champions.append(tournament_winner)

    return champions


def selection_with_roulette(slots_list, percentage):
    num_individuals = int(len(slots_list) * percentage)

    fitness_sum = 0
    for state in slots_list:
        fitness_sum += state.get_fitness()

    slots_list.sort(key=lambda x: state_order_function_roulette(x, fitness_sum))

    roulette_winners = []
    for i in range(num_individuals):
        roulette_winners.append(slots_list[i])

    return roulette_winners


def state_order_function_roulette(state, fitness_sum):
    return state.get_fitness() / fitness_sum

def state_order_function(state):
    return state.get_fitness()

def mutation_operator(state, probability, num_slots):
    # probability represents the probability of a mutation in each value of the list
    for i, slot in enumerate(state.get_slots()):
        if random.random() <= probability:
            while True:
                new_value = random.randrange(num_slots) + 1
                if new_value != slot:
                    break

            state.get_slots()[i] = new_value


def crossover_operator(state1, state2, incompatabilities):
    """
    Cross operator that creates a new allocation list,
    using roughly the same amount of information from both parents.
    """
    new_list = []

    slots1 = state1.get_slots()
    slots2 = state2.get_slots()

    for i in range(len(slots1)):
        if i % 2 == 0:
            new_list.append(slots1[i])
        else:
            new_list.append(slots2[i])

    new_state = State(incompatabilities, new_list)
    return new_state


def calc_solution_genetic_alg(incompatibilities, num_slots, num_subjects, num_generations, pop_size):

    # generate initial population
    population = []
    for _ in range(pop_size):
        population.append(State(incompatibilities, gen_random_allocation(num_slots, num_subjects)))


    # calculates a fixed number of generations
    for gen_number in range(num_generations):
        # order population given the fitness value
        population.sort(key=state_order_function)
        print("Start of generation {gen_number}. Best state: {state}".format(gen_number=gen_number, state=population[0]))


        # check if optimal solution has been reached
        if population[0].get_fitness() == 0:
            break

        # selection process
        # best_states = selection_with_tournament(population, 0.5)
        best_states = selection_with_roulette(population, 0.5)


        new_population = []

        # perform elitism: 1/5 of the best states pass through to the next generation
        num_elitism = pop_size // 5
        for i in range(num_elitism):
            new_population.append(population[i])


        # crossover process
        for _ in range(pop_size - num_elitism):

            while True:
                state1 = random.choice(best_states)
                state2 = random.choice(best_states)
                if state1 != state2:
                    break

            new_population.append(crossover_operator(state1, state2, incompatibilities))


        # mutation process
        for state in new_population:
            mutation_operator(state, 0.1, num_slots)

        population = new_population

    print("Last generation ({gen_number}). Best state: {state}".format(gen_number=num_generations, state=population[0]))
    print("Reached the end of the algorithm.")
    return population[0]
