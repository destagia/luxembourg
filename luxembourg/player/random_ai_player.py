from luxembourg.board import Board
from luxembourg.line  import Line
from luxembourg.point import Point

import random

class RandomAiPlayer:
    """
    CPU with Monte Carlo Approximation
    """

    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'
    DIAGONAL = 'diagonal'

    def __init__(self, board, symbol):
        self.__simple = simple
        self.__board = board
        self.__symbol = symbol
        self.__forwards = [self.HORIZONTAL, self.VERTICAL, self.DIAGONAL]

    def get_symbol(self):
        return self.__symbol

    def get_line(self):
        """
        Choose the line from empties randomly
        It is assumed this function will be used to advance
        the game randomly (without thinking)

        :return: random line (which can be drawn)
        """
        start_points = self.__board.get_empty_points()
        start        = random.choice(start_points)
        end          = start
        candidate    = start

        forward        = random.choice(self.__forwards)
        advancer       = self.get_forward_func(forward)
        end_candidates = []
        for _ in range(0, len(start_points) - 1):
            end = candidate
            end_candidates.append(end)
            candidate = advancer(end.get_x(), end.get_y())
            if not candidate in start_points:
                break

        end = random.choice(end_candidates)
        return Point(start, end)

    def get_forawrds(self):
        return self.forwards

    def get_forward_func(self, forward):
        if forward == self.HORIZONTAL:
            return self.get_forward_horizontally
        elif forward == self.VERTICAL:
            return self.get_forward_vertically
        elif forward == self.DIAGONAL:
            return self.get_forward_diagonally

    def get_forward_horizontally(self, p):
        return Point(p.get_x() + 1, p.get_y())

    def get_forward_vertically(self, p):
        return Point(p.get_x(), p.get_y() + 1)

    def get_forward_diagonally(self, p):
        return Point(p.get_x() + 1, p.get_y() + 1)

