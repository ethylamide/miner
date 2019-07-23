class BoardView:
    def __init__(self, board):
        self.board = board

    def render(self):
        for x in range(0, self.board.rows):
            row = " ".join([str(self.board.cell(x, y)) for y in range(0, self.board.cols)])
            print(row)
