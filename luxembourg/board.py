from functools import reduce

class Board:

    def __init__(self, depth):
        self.__board = []
        for row_count in range(1, depth + 1):
            self.__board.append([None for _ in range(0, row_count)])

    def get_none_count(self):
        sum = 0
        for row in self.__board:
            for value in row:
                if value == None:
                    sum += 1
        return sum

    def get_empty_points(self):
        points = []
        for row_index in range(0, len(self.__board)):
            for col_index in range(0, len(self.__board[row_index])):
                if self.__board[row_index][col_index] == None:
                    points.append((row_index, col_index))
        return points

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
            if self.__board[row][col] != None:
                raise RuntimeError('there has been already player')
            self.__board[row][col] = player

