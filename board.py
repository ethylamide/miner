import random

class Board:
    def __init__(self, rows = 26, cols = 13, mines = 75):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = ['.'] * (rows * cols)

        while mines > 0:
            x = random.randint(0, self.rows - 1)
            y = random.randint(0, self.cols - 1)
            if self.board[self.__idx__(x, y)] != 'X':
                self.board[self.__idx__(x, y)] = 'X'
                mines -= 1

    def calculate(self):
        # calculations
        for x in range(0, self.rows):
            for y in range(0, self.cols):
                if self.board[self.__idx__(x, y)] != 'X':
                    amount = 0

                    cells = [
                        self.__mine__(x - 1, y - 1),
                        self.__mine__(x - 1, y),
                        self.__mine__(x - 1, y + 1),
                        self.__mine__(x, y - 1),
                        self.__mine__(x, y + 1),
                        self.__mine__(x + 1, y - 1),
                        self.__mine__(x + 1, y),
                        self.__mine__(x + 1, y + 1)
                    ]

                    for val in cells:
                        amount += val

                    if amount > 0:
                        self.board[self.__idx__(x, y)] = amount

    def __idx__(self, x, y):
        return x * self.cols + y

    def __in_bound__(self, x, y):
        return ((x >= 0 and x < self.rows) and (y >= 0 and y < self.cols))

    def __mine__(self, x, y):
        if self.__in_bound__(x, y):
            if self.board[self.__idx__(x, y)] == 'X':
                return 1
            else:
                return 0
        else:
            return 0

    def cell(self, x, y):
        assert self.__in_bound__(x, y), "Board: Out of bound"
        return self.board[self.__idx__(x, y)]
