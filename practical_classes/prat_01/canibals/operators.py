from state import State

def take10(state):
    """
    Take a cannibal to the right side.
    """
    if state.cannibals < 1 or not state.boat:
        return None

    new_state = State(state.cannibals - 1, state.missionaries, not state.boat)

    return new_state if new_state.is_valid_state() else None


def take11(state):
    """
    Take a cannibal and a missionary to the right side.
    """
    if state.cannibals < 1 or state.missionaries < 1 or not state.boat:
        return None

    new_state = State(state.cannibals - 1, state.missionaries - 1, not state.boat)

    return new_state if new_state.is_valid_state() else None


def take20(state):
    """
    Take two cannibals to the right side.
    """
    if state.cannibals < 2 or not state.boat:
        return None

    new_state = State(state.cannibals - 2, state.missionaries, not state.boat)

    return new_state if new_state.is_valid_state() else None


def take01(state):
    """
    Take a missionary to the right side.
    """
    if state.missionaries < 1 or not state.boat:
        return None

    new_state = State(state.cannibals, state.missionaries - 1, not state.boat)

    return new_state if new_state.is_valid_state() else None


def take02(state):
    """
    Take two missionaries to the right side.
    """
    if state.missionaries < 2 or not state.boat:
        return None

    new_state = State(state.cannibals, state.missionaries - 2, not state.boat)

    return new_state if new_state.is_valid_state() else None


def bring10(state):
    """
    Take a cannibal to the left side.
    """
    if (3 - state.cannibals < 1) or state.boat:
        return None

    new_state = State(state.cannibals + 1, state.missionaries, not state.boat)

    return new_state if new_state.is_valid_state() else None


def bring11(state):
    """
    Take a cannibal and a missionary to the left side.
    """
    if (3 - state.cannibals < 1) or (3 - state.missionaries < 1) or state.boat:
        return None

    new_state = State(state.cannibals + 1, state.missionaries + 1, not state.boat)

    return new_state if new_state.is_valid_state() else None


def bring20(state):
    """
    Take two cannibals to the left side.
    """
    if (3 - state.cannibals < 2) or state.boat:
        return None

    new_state = State(state.cannibals + 2, state.missionaries, not state.boat)

    return new_state if new_state.is_valid_state() else None


def bring01(state):
    """
    Take a missionary to the left side.
    """
    if (3 - state.missionaries < 1) or state.boat:
        return None

    new_state = State(state.cannibals, state.missionaries + 1, not state.boat)

    return new_state if new_state.is_valid_state() else None


def bring02(state):
    """
    Take two missionaries to the left side.
    """
    if (3 - state.missionaries < 2) or state.boat:
        return None

    new_state = State(state.cannibals, state.missionaries + 2, not state.boat)

    return new_state if new_state.is_valid_state() else None


operators = [
    take01,
    take02,
    take10,
    take11,
    take20,
    bring01,
    bring02,
    bring10,
    bring11,
    bring20
]