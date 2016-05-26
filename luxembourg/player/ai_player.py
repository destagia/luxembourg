import random

class AiPlayer:
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'
    DIAGONAL = 'diagonal'

    def __init__(self, board):
        self.__board = board
        self.__forwards = [self.HORIZONTAL, self.VERTICAL, self.DIAGONAL]

    def get_symbol(self):
        return 'C'

    def get_line(self):
        return self.__get_random_line()

    def __get_random_line(self):
        start_points = self.__board.get_empty_points()
        start = random.choice(start_points)
        candidate = start
        forward = random.choice(self.__forwards)
        while candidate in start_points:
            end = candidate
            (end_x, end_y) = end
            if forward == self.HORIZONTAL:
                candidate = (end_x + 1, end_y)
            elif forward == self.VERTICAL:
                candidate = (end_x, end_y + 1)
            elif forward == self.DIAGONAL:
                candidate = (end_x + 1, end_y + 1)
        ((start_x, start_y), (end_x, end_y)) = (start, end)
        return (start_x, start_y, end_x, end_y)
