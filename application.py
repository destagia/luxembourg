from luxembourg.player.ai_player import AiPlayer
from luxembourg.player.controll_player import ControllPlayer
from luxembourg.judge import Judge
from luxembourg.board import Board

# Command line game

board = Board()
players = [ControllPlayer('1'), ControllPlayer('2')]
judge = Judge(board)
index = 0
while not judge.is_finished():
    player = players[index]
    (fx, fy, tx, ty) = player.get_line()
    try:
        board.draw_line(player, fx, fy, tx, ty)
    except RuntimeError as error:
        print(error)
        board.show()
        continue
    board.show()
    index = (index + 1) % 2
print ("Player " + player.get_symbol() + " won!")