from functools import reduce

class Board:

    def __init__(self, depth=None, board=None, hash=None, tag='main'):
        self.__tag = tag
        self.__board = []

        if board != None:
            for row in board.__board:
                self.__board.append([value for value in row])
        elif depth != None:
            for row_count in range(1, depth + 1):
                self.__board.append([None for _ in range(0, row_count)])
            if hash != None:
                for value in hash:
                    self.__board[value['y']][value['x']] = value['value']
        else:
            raise RuntimeError('Invalide initialization of Board')

    def get_tag(self):
        return self.__tag

    def get_none_count(self):
        sum = 0
        for row in self.__board:
            for value in row:
                if value == None:
                    sum += 1
        return sum

    def get_empty_points(self):
        """
        Return all empty point in this board
        Empty means that the array value is None

        :return: Array of all empty points
        """
        points = []
        for row_index in range(0, len(self.__board)):
            for col_index in range(0, len(self.__board[row_index])):
                if self.__board[row_index][col_index] == None:
                    points.append(Point(row_index, col_index))
        return points

    def show(self):
        """
        Show current board state to stdout
        """
        print('=======================')
        for row in self.__board:
            for player in row:
                if player == None:
                    print('.', end='')
                else:
                    print(player.get_symbol(), end='')
            print('')
        print('=======================')

    def draw_line(self, player, line):
        from_row = line.get_start().get_x()
        from_col = line.get_start().get_y()
        to_row   = line.get_end().get_x()
        to_col   = line.get_end().get_y()

        if from_row == to_row:
            # Veritcal line
            r = [(from_row, col) for col in range(from_col, to_col + 1)]
        elif from_col == to_col:
            # Horizontal line
            r = [(row, from_col) for row in range(from_row, to_row + 1)]
        else:
            # Lean line
            r = [(from_row + x, from_col + x) for x in range(0, to_row - from_row + 1)]

        for (row, col) in r:
            if self.__board[row][col] != None:
                raise RuntimeError('there has been already player')
            self.__board[row][col] = player

