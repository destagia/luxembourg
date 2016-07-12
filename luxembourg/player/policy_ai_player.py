from luxembourg        import Board, Line, Point
from luxembourg.policy import PolicyFunction, PolicyNetwork

import copy
import pickle
import random

class PolicyHistory:
    def __init__(self, state, action, probabilities):
        self.state = state
        self.action = action
        self.probabilities = probabilities

class PolicyAiPlayer:

    INPUT_SIZE = 15
    OUTPUT_SIZE = 75

    def __init__(self, board, symbol):
        self.lines = self.__create_lines()
        self.__symbol = symbol
        self.__board = board
        self.network = PolicyNetwork(PolicyAiPlayer.INPUT_SIZE,
                                     PolicyAiPlayer.OUTPUT_SIZE)
        self.__history = []

    def add_history(self, history):
        self.__history.append(history)

    def get_symbol(self):
        return self.__symbol

    def get_line(self):
        state = self.__board.get_as_single_array()
        state = map(lambda x: 1 if x != None else 0, state)
        while True: # search valid answer
            action, probabilities = self.network.get_action(state)
            selected_line = self.lines[action]
            stub_board = Board(board=self.__board)
            try:
                print(action)
                stub_board.draw_line(self, selected_line)
            except:
                self.network.learn(probabilities, [random.randint(0, 74)])
                continue
            break

        self.add_history(PolicyHistory(state, action, probabilities))
        return selected_line

    def reset(self, board):
        self.__history = []
        self.__board = board

    def on_lost_game(self):
        for data in self.__history:
            self.network.learn(data.probabilities, [data.action])

    def on_won_game(self):
        for data in self.__history:
            self.network.learn(data.probabilities, [data.action])

    def __create_lines(self):
        points = [Point(x, y) for x in range(0, 5) for y in range(0, 5) if x >= y]
        def distinct(acc, x):
            if not x in acc:
                acc.append(x)
            return acc
        def validate(acc, points):
            p1, p2 = points
            x_diff = p1.get_x() - p2.get_x()
            y_diff = p1.get_y() - p2.get_y()
            if x_diff == 0 or y_diff == 0 or x_diff == y_diff:
                if p2.get_x() < p1.get_x() or p2.get_y() < p1.get_y():
                    points = (p2, p1)
                acc.append(Line(points[0], points[1]))
            return acc
        lines = reduce(distinct, [set([x, y]) for x in range(0, 15) for y in range(0, 15)], [])
        lines = map(lambda x: list(x) + list(x) if len(x) == 1 else sorted(list(x)), lines)
        lines = map(lambda x: (points[x[0]], points[x[1]]), lines)
        lines = reduce(validate, lines, [])
        return lines



