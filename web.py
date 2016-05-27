from bottle import route, run, template, post, get
from bottle import request
from bottle import response
from luxembourg.player.ai_player import AiPlayer
from luxembourg.board import Board
import json

@route('/')
def index():
    return template('index')

@post('/luxembourg')
def luxembourg():
    board_json = json.loads(request.forms.get('board'))
    board = Board(depth=5, hash=board_json)
    cpu = AiPlayer(board)
    (sx, sy, ex, ey) = cpu.get_line()
    response.set_header('Content-Type', 'application/json')
    return json.dumps({
        'start': { 'x': sy, 'y': sx },
        'end': { 'x': ey, 'y': ex }
    })

run(host='localhost', port=8080, debug=True, reloader=True)