from luxembourg.player.ai_player import AiPlayer
from luxembourg.player.controll_player import ControllPlayer
from luxembourg.judge import Judge
from luxembourg.board import Board

def start_game():
    board = Board()
    players = [ControllPlayer('1'), ControllPlayer('2')]
    judge = Judge(board)
    index = 0
    while not judge.is_finished():
        player = players[index]
        (fx, fy, tx, ty) = player.get_line()
        board.draw_line(player, fx, fy, tx, ty)
        board.show()
        index = (index + 1) % 2