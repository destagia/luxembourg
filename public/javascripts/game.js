$(function () {
  var canvas = $('#lastone_canvas');
  var canvasWidth = canvas.width();
  var canvasHeight = canvas.height();
  var context = canvas.get(0).getContext('2d');

  var offset = 5;
  var start;
  var flag = false;

  var board = new Board(5);

  var clearCanvas = function () {
    context.clearRect(0, 0, canvasWidth, canvasHeight);
  };

  var arrangeSquare = function (board) {
    board.getSquares().forEach(function (square, index) {
      var defaultStyle = context.strokeStyle;
      context.beginPath();
      var x = square.getX();
      var y = square.getY();
      if (square.isSelected()) {
        context.strokeStyle = 'rgb(155, 187, 89)';
      } else if (square.hasValue()) {
        if (square.getValue() == 'player') {
          context.strokeStyle = 'rgb(255, 187, 130)';
        } else if (square.getValue() == 'CPU') {
          context.strokeStyle = 'rgb(187, 255, 130)';
        } else {
          console.log(square.getValue());
        }
      }

      context.moveTo(x, y - 20);
      context.lineTo(x, y + 20);
      context.stroke();
      context.closePath();
      context.strokeStyle = defaultStyle;
    });
  };

  var judge = function (turn) {
    if (board.getEmptySquares().length == 1) {
      alert(turn + "の勝ち");
    }
  };

  arrangeSquare(board);

  var squares = null;
  canvas.mousedown(function (e) {
    flag = true;
    var startX = e.pageX - $(this).offset().left - offset;
    var startY = e.pageY - $(this).offset().top - offset;
    start = board.getNeighboor(startX, startY);
    squares = board.getSquares();
    return false;
  });

  canvas.mousemove(function (e) {
    if (flag) {
      var endX = e.pageX - $('canvas').offset().left - offset;
      var endY = e.pageY - $('canvas').offset().top - offset;
      squares.forEach(function (s) { s.setSelected(false); });
      var end = board.getNeighboor(endX, endY);
      start.setSelected(true);

      var startIndex = start.getIndex();
      var endIndex = end.getIndex();
      if (startIndex.y == endIndex.y) {
        for (var i = Math.min(startIndex.x, endIndex.x); i <= Math.max(startIndex.x, endIndex.x); i++) {
          var s = board.getSquareWithIndex(i, startIndex.y);
          if (s.hasValue()) {
            break;
          }
          s.setSelected(true);
        }
      } else if (startIndex.x == endIndex.x) {
        for (var i = Math.min(startIndex.y, endIndex.y); i <= Math.max(startIndex.y, endIndex.y); i++) {
          var s = board.getSquareWithIndex(startIndex.x, i);
          if (s.hasValue()) {
            break;
          }
          s.setSelected(true);
        }
      } else if (startIndex.x - endIndex.x == startIndex.y - endIndex.y) {
        var minX = Math.min(startIndex.x, endIndex.x);
        var maxX = Math.max(startIndex.x, endIndex.x);
        var minY = Math.min(startIndex.y, endIndex.y);
        for (var i = startIndex.x; i <= maxX; i++) {
          var s = board.getSquareWithIndex(i, minY + i - minX);
          if (s.hasValue()) {
            break;
          }
          s.setSelected(true);
        }
      }

      clearCanvas();
      arrangeSquare(board);
      context.lineWidth = 2;
      context.beginPath();
      context.moveTo(start.getX(), start.getY());
      context.lineTo(endX, endY);
      context.stroke();
      context.closePath();
    }
  });

  var decide = function () {
    if (!flag) {
      return;
    }
    board.applySelectedSquare('player');
    clearCanvas();
    arrangeSquare(board);
    judge('player');

    $.ajax({
      url: '/luxembourg',
      type: 'post',
      data: 'json',
      data: {
        board: board.toJSON(),
      },
    })
    .success(function (line) {
      console.log(line);
      var squares = [];
      if (line.start.x == line.end.x) {
        for (var i = line.start.y; i <= line.end.y; i++) {
          squares.push(board.getSquareWithIndex(line.start.x, i));
        }
      } else if (line.start.y == line.end.y) {
        for (var i = line.start.x; i <= line.end.x; i++) {
          squares.push(board.getSquareWithIndex(i, line.start.y));
        }
      } else {
        for (var x = line.start.x; x <= line.end.x; x++) {
          squares.push(board.getSquareWithIndex(x, x + line.start.y - line.start.x));
        }
      }
      squares.forEach(function (s) {
        s.setValue('CPU');
      });
      clearCanvas();
      arrangeSquare(board);
      judge('CPU');
    });
    flag = false;
  };

  canvas.on('mouseup', function () {
    decide();
  });

  canvas.on('mouseleave', function () {
    decide();
  });

});