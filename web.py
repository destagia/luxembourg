from bottle import route, run, template, post, get
from bottle import request
from bottle import response
from bottle import static_file
from luxembourg.player.ai_player import AiPlayer
from luxembourg.board import Board
import json
import os

@route('/public/<filepath:path>')

@route('/public/<filepath:path>', name='static_file')
def static(filepath):
    return static_file(filepath, root="./public")

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

HOST     = os.environ.get("BOTTLE_HOST",     'localhost')
PORT     = os.environ.get("BOTTLE_PORT",     8080)
DEBUG    = os.environ.get("BOTTLE_DEBUG",    True)
RELOADER = os.environ.get("BOTTLE_RELOADER", True)

print("Start Application 🏰")
print("[info] host: {0}, port: {1}".format(HOST, PORT))

run(host=HOST, port=PORT, debug=DEBUG, reloader=RELOADER)