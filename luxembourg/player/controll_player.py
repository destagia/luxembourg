from luxembourg.line  import Line
from luxembourg.point import Point

class ControllPlayer:
    """
    Player controlled by human
    """
    def __init__(self, symbol):
        """
        Initialize ControllPlayer
        :param symbol: String for identifying each player
        """
        self.__symbol = symbol

    def get_symbol(self):
        """
        Get player's symbol to identify
        :return: Symbol which is passed when initializing
        """
        return self.__symbol

    def get_line(self):
        """
        Get the next line for the game

        :return: Tuple representing a line
        """
        print('input from x position')
        from_row = int(input())
        print('input from y position')
        from_col = int(input())
        print('input to x position')
        to_row = int(input())
        print('input to y position')
        to_col = int(input())
        return Line(Point(from_row, from_col), Point(to_row, to_col))