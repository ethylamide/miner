from queue import *

class GameState:
    def __init__(self, board):
        self.board = board
        self.marked_mines = 0
        self.is_over = False
        self.explosed = False

    def open_cell(self, x, y):
        """Open cell at given point"""

        # if marked or opened - do nothing
        # else:
        # check cell on bomb
        # if bomb self.is_over = True
        # else if cell have number - just open 1 cell
        # else open all blank cells connected to current blank cell
        #      and open cells that are neightbored to blank cells

        cell = self.board.cell(x, y)

        if not cell.is_showed() or cell.is_marked():
            cell.show()
            if cell.is_mined():
                self.explosed = True
            elif cell.is_blank():
                self.discover_cells(x, y)

    def mark_cell(self, x, y):
        """Open cell at given point with bomb"""

        # check cell if it opened before - do nothing
        # else mark cell as bomb if unmarked
        # else unmark if marked

        self.board.cell(x, y).toggleMark()


    def discover_cells(self, x, y):
        # open all blank cells connected to current blank cell
        # and open cells that are neightbored to blank cells

        visited = set()
        queue = Queue()

        self.board.cell(x, y).show()

        for p in self.board.neighbors(x, y):
            cell = self.board.cell(p[0], p[1])
            if not cell.is_showed():
                if cell.is_blank():
                    queue.push((p[0], p[1]))
                # open num cells
                if cell.is_valued():
                    cell.show()

        visited.add((x, y))

        while not queue.isEmpty():
            (nx, ny) = queue.pop()
            if not (nx, ny) in visited:
                self.board.cell(nx, ny).show()
                visited.add((nx, ny))

                for p in self.board.neighbors(nx, ny):
                    if not p in visited:
                        cell = self.board.cell(p[0], p[1])
                        if not cell.is_showed():
                            if cell.is_blank():
                                queue.push((p[0], p[1]))
                            # open num cells
                            if cell.is_valued():
                                cell.show()

    def discover_cell(self, x, y):
        """Open closed cells around given point"""

        # if not opened - do nothing
        # else
        # check that point have proper marked cells around
        # open all closed neightbored cells

        cell = self.board.cell(x, y)

        if cell.is_showed() and cell.is_valued():
            neighbors = self.board.neighbors(x, y)

            amount = 0
            for p in neighbors:
                if self.board.cell(p[0], p[1]).is_mined():
                    amount += 1

            if amount == cell.number_of_mines():
                for p in neighbors:
                    self.open_cell(p[0], p[1])

    def is_game_over(self):
        """Check is game over"""

        return self.is_over or self.explosed
