import random
from cell import Cell

class Board:
    def __init__(self, rows = 26, cols = 13, mines = 75):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = []

        for _ in range(0, rows * cols):
            self.board.append(Cell())

        while mines > 0:
            x = random.randint(0, self.rows - 1)
            y = random.randint(0, self.cols - 1)

            cell = self.board[self._idx(x, y)]

            if not cell.is_mined():
                self.board[self._idx(x, y)] = Cell(mined=True)
                mines -= 1

    def calculate(self):
        # calculations
        for x in range(0, self.rows):
            for y in range(0, self.cols):
                cell = self.board[self._idx(x, y)]

                if not cell.is_mined():
                    cells = list(filter(lambda p: self.cell(p[0], p[1]).is_mined(), self.neighbors(x, y)))
                    amount = len(cells)

                    if amount > 0:
                        self.board[self._idx(x, y)] = Cell(value=amount)
                        if cell.is_showed():
                            self.board[self._idx(x, y)].show()

    def cell(self, x, y):
        assert self._is_in_bound(x, y), "Board: Out of bound"
        return self.board[self._idx(x, y)]

    def _idx(self, x, y):
        return x * self.cols + y

    def _is_in_bound(self, x, y):
        return ((x >= 0 and x < self.rows) and (y >= 0 and y < self.cols))

    def neighbors(self, x, y):
         points = [(x - 1, y - 1),
                   (x - 1, y),
                   (x - 1, y + 1),
                   (x, y - 1),
                   (x, y + 1),
                   (x + 1, y - 1),
                   (x + 1, y),
                   (x + 1, y + 1)]
         return list(filter(lambda p: self._is_in_bound(p[0], p[1]), points))
