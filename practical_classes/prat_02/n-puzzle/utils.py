def create_board(number):
    if number == 1:
        return [
            [1, 2, 3],
            [5, 0, 6],
            [4, 7, 8]
        ]

    elif number == 2:
        return [
            [1, 3, 6],
            [5, 2, 0],
            [4, 7, 8]
        ]

    elif number == 3:
        return [
            [1, 6, 2],
            [5, 7, 3],
            [0, 4, 8]
        ]

    elif number == 4:
        return [
            [5, 1, 3, 4],
            [2, 0, 7, 8],
            [10, 6, 11, 12],
            [9, 13, 14, 15]
        ]

    else:
        return None