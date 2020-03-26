import math
import random


def hill_climbing(state, incompatibilities, num_slots, max_num_iters):
    """
    Performs the hill climbing algorithm with a maximum number of
    iterations, or until it gets to a (maybe local) maximum.

    In regular hill climbing, neighbours are generated one
    by one. If a new neighbour has higher, it is chosen
    as the current state (greedy approach).
    """
    num_iters = 0
    cur_state = state
    if cur_state.get_score() == 0: # initial state was already best state!
        return cur_state

    print("Initial state: {state}".format(state=cur_state))

    while num_iters < max_num_iters:
        found_better_state = False
        for neighbour in cur_state.generate_neighbours(incompatibilities, num_slots):
            print("New neighbour state: {state}".format(state=neighbour))
            if neighbour.get_score() < cur_state.get_score(): # found a better state
                cur_state = neighbour
                found_better_state = True
                print("New current state: {state}. It number {n}".format(state=cur_state, n=num_iters))

                if cur_state.get_score() == 0: # reached best state!
                    return cur_state

                break

        num_iters += 1
        if not found_better_state: # if none of the current state's neighbours are better than it, return
            return cur_state       # the current state.


    return cur_state


def steepest_ascent_hill_climbing(state, incompatibilities, num_slots, max_num_iters):
    """
    Performs the hill climbing algorithm with a maximum number of
    iterations, or until it gets to a (maybe local) maximum.

    In steepest ascent hill climbing, all the neighbours of the current state
    are calculated, and the best one is chosen.
    """
    num_iters = 0
    cur_state = state
    if cur_state.get_score() == 0: # initial state was already best state!
        return cur_state

    print("Initial state: {state}".format(state=cur_state))

    while num_iters < max_num_iters:
        found_better_state = False
        best_state = cur_state
        for neighbour in cur_state.generate_neighbours(incompatibilities, num_slots):
            print("New neighbour state: {state}".format(state=neighbour))
            if neighbour.get_score() < best_state.get_score(): # found a better state
                best_state = neighbour
                found_better_state = True
                print("New best state: {state}".format(state=best_state))

                if best_state.get_score() == 0: # reached best state!
                    return best_state

        num_iters += 1
        if found_better_state:
            cur_state = best_state
            print("New current state: {state}. It number {n}".format(state=cur_state, n=num_iters))
        else:                # if none of the current state's neighbours are better than it, return
            return cur_state # the current state.


    return cur_state


def simulated_annealing(state, incompatibilities, num_slots, annealing_step):
    """
    Calculates the solution using simulated annealing.
    """
    num_iters = 0
    cur_state = state
    gen = cur_state.generate_neighbours(incompatibilities, num_slots)

    if cur_state.get_score() == 0: # initial state was already best state!
        return cur_state

    print("Initial state: {state}".format(state=cur_state))

    while True:
        temperature = 1 - num_iters * annealing_step
        if temperature <= 0: return cur_state

        try:
            neighbour = next(gen)
            print("New neighbour state: {state}".format(state=neighbour))
        except StopIteration: # no more items
            return cur_state

        if neighbour.get_score() < cur_state.get_score():
            cur_state = neighbour
            gen = cur_state.generate_neighbours(incompatibilities, num_slots)
            print("New current state: {state}. It number {n}".format(state=cur_state, n=num_iters))
        else:
            delta = (cur_state.get_score() - neighbour.get_score()) / (neighbour.get_score() + cur_state.get_score())
            probability = math.exp(delta / temperature)
            if probability > 1: probability = 1
            print("Prob: {prob}; delta={delta}; temp={temp}".format(prob=probability, delta=delta, temp=temperature))
            if random.random() <= probability:
                cur_state = neighbour
                gen = cur_state.generate_neighbours(incompatibilities, num_slots)
                print("New (worse) current state: {state}. It number {n}".format(state=cur_state, n=num_iters))

        num_iters += 1

