import random

class AiPlayer:
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'
    DIAGONAL = 'diagonal'

    def __init__(self, board, symbol):
        self.__board = board
        self.__symbol = symbol
        self.__forwards = [self.HORIZONTAL, self.VERTICAL, self.DIAGONAL]

    def get_symbol(self):
        return self.__symbol

    def get_line(self):
        return self.__get_random_line()

    def __get_random_line(self):
        start_points = self.__board.get_empty_points()
        start = random.choice(start_points)
        candidate = start

        forward = random.choice(self.__forwards)
        if forward == self.HORIZONTAL:
            advancer = self.__get_forward_horizontally
        elif forward == self.VERTICAL:
            advancer = self.__get_forward_vertically
        elif forward == self.DIAGONAL:
            advancer = self.__get_forward_diagonally

        for _ in range(0, len(start_points) - 1):
            end = candidate
            (end_x, end_y) = end
            candidate = advancer(end_x, end_y)
            if not candidate in start_points:
                print('Advance too much!')
                break
            if random.randint(0, 100) < 20:
                print('random break!')
                break

        ((start_x, start_y), (end_x, end_y)) = (start, end)
        return (start_x, start_y, end_x, end_y)

    def __get_forward_horizontally(self, x, y):
        return (x + 1, y)

    def __get_forward_vertically(self, x, y):
        return (x, y + 1)

    def __get_forward_diagonally(self, x, y):
        return (x + 1, y + 1)
