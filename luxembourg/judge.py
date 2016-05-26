class Judge:

    def __init__(self, board):
        self.__board = board

    def is_finished(self):
        return self.__board.get_none_count() == 1
