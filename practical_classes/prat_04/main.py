from prat_04.utils import read_from_file

if __name__ == '__main__':
    state = read_from_file('info.txt')

    for key, value in state.get_incompatibilities().items():
        print("{key} -> {value}".format(key=key, value=value))
