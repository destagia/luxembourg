function Board (count) {
  count = count || 5;
  this.field = [];
  for (var i = 0; i < count; i++) {
    row = [new Square(null, 0, i)]
    for (var j = 0; j < i; j++) {
      row.push(new Square(null, j + 1, i))
    }
    this.field.push(row);
  }
}

Board.prototype.getSquareWithIndex = function (indexX, indexY) {
  return this.field[indexY][indexX];
};
Board.prototype.getSquares = function () {
  var squares = [];
  for (var i = 0; i < this.field.length; i++) {
    var row = this.field[i];
    for (var j = 0; j < row.length; j++) {
      squares.push(row[j]);
    }
  }
  return squares;
};

Board.prototype.getNeighboor = function (x, y) {
  var min = null;
  var minMagnitude = null;
  this.getSquares().forEach(function (s) {
    if (s.getValue() != null) {
      return;
    }
    if (min == null) {
      min = s;
      minMagnitude = s.getMagnitudeSqr(x, y);
      return;
    }
    var mag = s.getMagnitudeSqr(x, y);
    if (mag < minMagnitude) {
      min = s;
      minMagnitude = mag;
    }
  });
  return min;
};

Board.prototype.applySelectedSquare = function (value) {
  this.getSquares().forEach(function (s) {
    if (s.isSelected()) {
      s.setValue(value);
    }
  });
};

Board.prototype.getEmptySquares = function () {
  return this.getSquares().filter(function (value) { return !value.hasValue(); })
};

Board.prototype.toJSON = function () {
  return JSON.stringify(this.getSquares());
};