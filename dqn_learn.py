#!/usr/bin/env python

from luxembourg        import Judge, Board
from luxembourg.player import RandomAiPlayer, DqnAiPlayer

count = 0

players = [
    RandomAiPlayer(None, 'B'),
    DqnAiPlayer(None, 'A')
]

for no in range(0, 10000000):
    board = Board(depth=5)
    judge = Judge(board)

    print("- - Start New Game - -")

    for p in players:
        p.reset(board)

    index = 0
    while board.get_none_count() > 0:
        player = players[index]
        line = player.get_line()
        try:
            board.draw_line(player, line)
        except RuntimeError as error:
            print(error)
            board.show()
            continue
        board.show()
        index = (index + 1) % 2

    if index == 0:
        count += 1
    print(str(count) + " / " + str(no + 1))
