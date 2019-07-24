from board import *
from game import *
from view import *

board = Board()
board.calculate()

game = GameState(board)
for _ in range(0, 100):
    game.open_cell(random.randint(0, board.rows - 1),
                   random.randint(0, board.cols - 1))
view = BoardView(board)

view.render()
