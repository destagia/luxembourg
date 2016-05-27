from luxembourg.board import Board

import random

class AiPlayer:
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'
    DIAGONAL = 'diagonal'

    def __init__(self, board, symbol='X', simple=False):
        self.__simple = simple
        self.__board = board
        self.__symbol = symbol
        self.__forwards = [self.HORIZONTAL, self.VERTICAL, self.DIAGONAL]

    def get_symbol(self):
        return self.__symbol

    def get_line(self):
        if self.__simple:
            return self.__get_random_line()

        board = self.__board
        candidates = []

        for (sx, sy, ex, ey) in self.__get_all_forwards(board):
            win_count = 0
            stub_board = Board(board=board, tag='stub')
            self.__board = stub_board
            stub_board.draw_line(self, sx, sy, ex, ey)
            start = (sx, sy)

            points_count = len(self.__board.get_empty_points())
            if points_count > 1:
                for _ in range(0, (15 - points_count) * 100):
                    self.__board = Board(board=stub_board, tag='test' + str(_))
                    for player in self.__player_selector(self.__board):
                        (sx, sy, ex, ey) = player.__get_random_line()
                        self.__board.draw_line(player, sx, sy, ex, ey)
                        if len(self.__board.get_empty_points()) == 1:
                            break
                    if player == self:
                        win_count = win_count + 1
            elif points_count == 1:
                win_count = (15 - points_count) * 100
            else:
                win_count = 0
            candidates.append(((sx, sy, ex, ey), win_count))

        self.__board = board
        candidates.sort(key=lambda candidate: -candidate[1])
        print(candidates)
        return candidates[0][0]

    def __get_all_forwards(self, board):
        points = board.get_empty_points()
        for start in points:
            yield (start[0], start[1], start[0], start[1])
            for forward in self.__forwards:
                advancer = self.__get_forward_func(forward)
                end = start
                while True:
                    end = advancer(end[0], end[1])
                    if not end in points:
                        break
                    if start[0] != end[0] or start[1] != end[1]:
                        yield (start[0], start[1], end[0], end[1])


    def __player_selector(self, board):
        players = [AiPlayer(board), self]
        index = 0
        while True:
            yield players[index]
            index = (index + 1) % 2


    def __get_random_line(self, start=None):
        start_points = self.__board.get_empty_points()
        if start == None:
            start = random.choice(start_points)
        end = start
        candidate = start

        forward = random.choice(self.__forwards)
        advancer = self.__get_forward_func(forward)

        for _ in range(0, len(start_points) - 1):
            end = candidate
            (end_x, end_y) = end
            candidate = advancer(end_x, end_y)
            if not candidate in start_points:
                break
            if random.randint(0, 100) < 20:
                break

        ((start_x, start_y), (end_x, end_y)) = (start, end)
        return (start_x, start_y, end_x, end_y)

    def __get_forward_func(self, forward):
        if forward == self.HORIZONTAL:
            return self.__get_forward_horizontally
        elif forward == self.VERTICAL:
            return self.__get_forward_vertically
        elif forward == self.DIAGONAL:
            return self.__get_forward_diagonally

    def __get_forward_horizontally(self, x, y):
        return (x + 1, y)

    def __get_forward_vertically(self, x, y):
        return (x, y + 1)

    def __get_forward_diagonally(self, x, y):
        return (x + 1, y + 1)
