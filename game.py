import random
from queue import Queue


class GameState:
    def __init__(self, board):
        self.board = board
        self.marked_mines = 0
        self.is_over = False
        self.explosed = False
        self._opened = 0

    def open_cell(self, x, y):
        """Open cell and discover cells around if not a bomb"""

        cell = self.board.cell(x, y)

        if not (cell.is_showed() or cell.is_marked()):
            self._opened += 1
            cell.show()
            if cell.is_mined():
                self.explosed = True
            elif cell.is_blank():
                self._discover_cells(x, y)
        self.is_over = self._opened == self.board.rows * self.board.cols - self.board.mines

    def mark_cell(self, x, y):
        """Mark or unmark cell"""

        self.board.cell(x, y).toggleMark()

    def discover_cell(self, x, y):
        """Open closed cells around given point"""

        cell = self.board.cell(x, y)

        if cell.is_showed() and cell.is_valued():
            neighbors = self.board.neighbors(x, y)

            amount = 0
            for p in neighbors:
                if self.board.cell(p[0], p[1]).is_marked():
                    amount += 1

            if amount == cell.number_of_mines():
                for p in neighbors:
                    self.open_cell(p[0], p[1])

    def opened(self):
        self._opened

    def get_random_blank_cell(self):
        cells = []
        for x in range(0, self.board.rows):
            for y in range(0, self.board.cols):
                if self.board.cell(x, y).is_blank():
                    cells.append((x, y))

        idx = random.randint(0, len(cells) - 1)
        return cells[idx]

    def is_game_over(self):
        """Check is game over"""

        return self.is_over or self.explosed

    def _discover_cells(self, x, y):
        visited = set()
        queue = Queue()

        for p in self.board.neighbors(x, y):
            cell = self.board.cell(p[0], p[1])
            if not cell.is_showed():
                if cell.is_blank():
                    queue.push((p[0], p[1]))
                # open num cells
                if cell.is_valued():
                    self._opened += 1
                    cell.show()

        visited.add((x, y))

        while not queue.isEmpty():
            (nx, ny) = queue.pop()
            if not (nx, ny) in visited:
                self._opened += 1
                self.board.cell(nx, ny).show()
                visited.add((nx, ny))

                for p in self.board.neighbors(nx, ny):
                    if p not in visited:
                        cell = self.board.cell(p[0], p[1])
                        if not cell.is_showed():
                            if cell.is_blank():
                                queue.push((p[0], p[1]))
                            # open num cells
                            if cell.is_valued():
                                self._opened += 1
                                cell.show()
