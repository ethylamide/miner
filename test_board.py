import unittest
import random
from board import Board
from view import BoardView


class TestBoard(unittest.TestCase):
    def test_board_calculation(self):
        random.seed(10)
        board = Board(rows=4, cols=4, mines=3)

        for cell in board.board:
            cell.show()

        BoardView(board).render()
        board.calculate()
        print()
        BoardView(board).render()

        self.assertEqual(list(map(lambda c: str(c), board.board[0:4])),
                         ['.', '.', '2', 'X'], "First row should equal")
        self.assertEqual(list(map(lambda c: str(c), board.board[4:8])),
                         ['.', '.', '2', 'X'], "Second row should equal")
        self.assertEqual(list(map(lambda c: str(c), board.board[8:12])),
                         ['1', '1', '1', '1'],       "Third row should equal")
        self.assertEqual(list(map(lambda c: str(c), board.board[12:16])),
                         ['X', '1', '.', '.'], "Fourth row should equal")


if __name__ == '__main__':
    unittest.main()
