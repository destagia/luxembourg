from luxembourg.player.montec_ai_player import MonteCarloAiPlayer
from luxembourg.player.random_ai_player import RandomAiPlayer
from luxembourg.player.controll_player  import ControllPlayer
from luxembourg.judge import Judge
from luxembourg.board import Board

# Command line game

count = 0

for no in range(0, 100):
    board = Board(depth=5)
    players = [
        RandomAiPlayer(board, 'B'),
        MonteCarloAiPlayer(board, 'A')
    ]
    judge = Judge(board)
    index = 0
    while not judge.is_finished():
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