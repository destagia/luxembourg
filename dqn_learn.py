#!/usr/bin/env python

from luxembourg        import Judge, Board
from luxembourg.player import RandomAiPlayer, PolicyAiPlayer, ControllPlayer

count = 0

players = [
    RandomAiPlayer(None, 'B'),
    PolicyAiPlayer(None, 'A')
]

while True:
    for no in range(0, 50000):
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
                continue
            index = (index + 1) % 2


        if index == 0: # Player 0 won! 1 lost!
            count += 1
            players[0].on_won_game()
            players[1].on_lost_game()
        else:
            players[0].on_lost_game()
            players[1].on_won_game()

        print(str(count) + " / " + str(no + 1))

    players[0] = ControllPlayer("M")
