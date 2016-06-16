class Point:

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_x(self):
        self.__x

    def get_y(self):
        self.__y

    def to_dict(self):
        { x: self.__x, y: self.__y }
