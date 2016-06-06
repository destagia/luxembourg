function Square (value, x, y) {
  this.value = null;
  this.x = x;
  this.y = y;
  this.selected = false;
}

Square.prototype.isPlayer = function () {
  return this.value != null;
};

Square.prototype.getX = function () { return this.x * 50 + ((5 - this.y) * 25) + 100; };
Square.prototype.getY = function () { return this.y * 50 + 100; };

Square.prototype.getIndex = function () { return { x: this.x, y: this.y }; }

Square.prototype.setSelected = function (selected) { this.selected = selected; }
Square.prototype.isSelected = function () {
  if (this.hasValue()) {
    return false;
  }
  return this.selected;
}

Square.prototype.setValue = function (value) { this.value = value; }
Square.prototype.getValue = function () { return this.value; }
Square.prototype.hasValue = function () { return this.value != null; }

Square.prototype.getMagnitudeSqr = function (x, y) {
  return (this.getX() - x) * (this.getX() - x) + (this.getY() - y) * (this.getY() - y);
}