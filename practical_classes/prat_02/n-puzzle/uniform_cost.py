from operators import *
from state import *
from utils import *

if __name__ == '__main__':
    cur_state = State(create_board(4)) # current state (initialized with the initial state)

    states = [cur_state]  # list of states chosen
    potencial_states = []  # list of potencial states that were not yet explored

    # main loop
    while True:

        # if the current state is the final, break
        if cur_state.is_final_state():
            break

        # generate new potencial state for each operator
        for op in operators:
            new_state = op(cur_state)  # new state

            if new_state is not None:
                unique = True

                for state in states:
                    if state == new_state:  # in order to avoid the repetition of states
                        unique = False

                if unique:
                    new_state.set_parent(cur_state)
                    potencial_states.append(new_state)
                    potencial_states.sort(key=get_uniform_cost_value)

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
        state.print_state()