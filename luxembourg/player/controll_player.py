class ControllPlayer:

    def __init__(self, symbol):
        self.__symbol = symbol

    def get_symbol(self):
        return self.__symbol

    def get_line(self):
        print('input from x position')
        from_row = int(input())
        print('input from y position')
        from_col = int(input())
        print('input to x position')
        to_row = int(input())
        print('input to y position')
        to_col = int(input())
        return (from_row, from_col, to_row, to_col)