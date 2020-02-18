from state import State
import copy

if __name__ == '__main__':
    cur_state = State(0, 0) # current state (initialized with the initial state)
    states = [cur_state] # list of states chosen
    potencial_states = [] # list of potencial states that were not yet explored

    # main loop
    while True:

        # if the current state is the final, break
        if cur_state.is_final_state():
            break

        # generating new states
        new_state = cur_state.empty_first(states)
        if new_state is not None:
            new_state.set_parent(copy.copy(cur_state))
            potencial_states.append(new_state)

        new_state = cur_state.empty_second(states)
        if new_state is not None:
            new_state.set_parent(copy.copy(cur_state))
            potencial_states.append(new_state)

        new_state = cur_state.fill_first(states)
        if new_state is not None:
            new_state.set_parent(copy.copy(cur_state))
            potencial_states.append(new_state)

        new_state = cur_state.fill_second(states)
        if new_state is not None:
            new_state.set_parent(copy.copy(cur_state))
            potencial_states.append(new_state)

        new_state = cur_state.transf_12_empty(states)
        if new_state is not None:
            new_state.set_parent(copy.copy(cur_state))
            potencial_states.append(new_state)

        new_state = cur_state.transf_12_full(states)
        if new_state is not None:
            new_state.set_parent(copy.copy(cur_state))
            potencial_states.append(new_state)

        new_state = cur_state.transf_21_empty(states)
        if new_state is not None:
            new_state.set_parent(copy.copy(cur_state))
            potencial_states.append(new_state)

        new_state = cur_state.transf_21_full(states)
        if new_state is not None:
            new_state.set_parent(copy.copy(cur_state))
            potencial_states.append(new_state)


        if not potencial_states:
            print("No solution")
            break

        # choose next state
        cur_state = potencial_states.pop(0)
        states.append(cur_state)


    # output result
    output = []
    while cur_state is not None:
        output.insert(0, cur_state)
        cur_state = cur_state.parent


    for state in output:
        print(state)