from functools import reduce

class Board:

    def __init__(self):
        self.__board = [
            [None],
            [None, None],
            [None, None, None],
            [None, None, None, None],
            [None, None, None, None, None]
        ]

    def get_none_count(self):
        sum = 0
        for row in self.__board:
            for value in row:
                if value == None:
                    sum += 1
        return sum

    def show(self):
        for row in self.__board:
            for player in row:
                if player == None:
                    print('.', end='')
                else:
                    print(player.get_symbol(), end='')
            print('')

    def draw_line(self, player, from_row, from_col, to_row, to_col):
        if from_row > to_row or from_col > to_col:
            raise RuntimeError('from position must be smaller than to position')

        if from_row == to_row:
            r = [(from_row, col) for col in range(from_col, to_col + 1)]
        elif from_col == to_col:
            r = [(row, from_col) for row in range(from_row, to_row + 1)]
        else:
            r = [(from_row + x, from_col + x) for x in range(0, to_row - from_row + 1)]

        for (row, col) in r:
            self.__board[row][col] = player

