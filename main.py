from board import *
from view import *

board = Board()
board.calculate()
view = BoardView(board)

view.render()
