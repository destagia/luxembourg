from luxembourg.board                   import Board
from luxembourg.line                    import Line
from luxembourg.point                   import Point
from luxembourg.player.random_ai_player import RandomAiPlayer

import random

class MonteCarloAiPlayer(RandomAiPlayer):
    """
    CPU with Monte Carlo Approximation
    """

    def __init__(self, board, symbol):
        RandomAiPlayer.__init__(self, board, symbol)

    def get_line(self):
        board = self.get_board()
        candidates = []

        for line in self.__get_all_forwards(board):
            win_count = 0
            stub_board = Board(board=board)
            stub_board.draw_line(self, line)

            points_count = len(stub_board.get_empty_points())
            epoc_count =  (15 - points_count) * 100
            if points_count > 1:
                for _ in range(0, epoc_count):
                    epoc_board = Board(board=stub_board)
                    enemy_player = RandomAiPlayer(epoc_board, 'enemy')
                    me_player    = RandomAiPlayer(epoc_board, self.get_symbol())
                    for player in self.player_selector(enemy_player, me_player):
                        next_line = player.get_line()
                        epoc_board.draw_line(player, next_line)
                        if len(epoc_board.get_empty_points()) == 1:
                            break
                    if player.get_symbol() == self.get_symbol():
                        win_count = win_count + 1
            elif points_count == 1:
                win_count = epoc_count
            else:
                win_count = 0
            candidates.append((line, win_count))

        candidates.sort(key=lambda candidate: -candidate[1])
        print(candidates)
        return candidates[0][0]

    def on_lost_game(self):
        pass

    def on_won_game(self):
        pass

    def __get_all_forwards(self, board):
        """
        Calculate and get all candidates which can be drawn

        :param board: Board object is required where the lines can be drawn
        :return     : Iterator of lines (use this with for syntax)
        """
        points = board.get_empty_points()
        for start in points:
            yield Line(start, start)
            for forward in self.get_forwards():
                advancer = self.get_forward_func(forward)
                end = start
                while True:
                    end = advancer(end)
                    if not end in points:
                        break
                    if start != end:
                        yield Line(start, end)

    def player_selector(self, player_a, player_b):
        """
        Return Interator which returns other player subsequently
        Inifinite Array [player_a, player_b, player_a, ...]

        :param player_a: first player
        :param player_b: second player
        :return        : Iterator which returns given players alternatively
        """
        players = [player_a, player_b]
        index = 0
        while True:
            yield players[index]
            index = (index + 1) % 2