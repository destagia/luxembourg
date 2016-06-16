class Point:

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def __eq__(self, other):
        return isinstance(other, Point) and self.get_x() == other.get_x() and self.get_y() == other.get_y()

    def __str__(self):
        return "(" + str(self.__x) + ", " + str(self.__y) + ")"

    __repr__ = __str__

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def to_dict(self):
        return { x: self.__x, y: self.__y }
