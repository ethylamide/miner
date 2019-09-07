import random
import unittest

from board import Board

from game import GameState
# from view import BoardView


class TestGame(unittest.TestCase):
    def test_open_cell(self):
        random.seed(10)

        # print("Test open cell:")
        board = Board(rows=4, cols=4, mines=3)
        board.calculate()
        game = GameState(board)
        game.open_cell(0, 0)
        # BoardView(board).render()

        self.assertEqual(list(map(lambda c: str(c), board.board[0:4])),
                         ['.', '.', '2', ' '], "First row should equal")
        self.assertEqual(list(map(lambda c: str(c), board.board[4:8])),
                         ['.', '.', '2', ' '], "Second row should equal")
        self.assertEqual(list(map(lambda c: str(c), board.board[8:12])),
                         ['1', '1', '1', ' '],       "Third row should equal")
        self.assertEqual(list(map(lambda c: str(c), board.board[12:16])),
                         [' ', ' ', ' ', ' '], "Fourth row should equal")

        # print()

    def test_discover_cell(self):
        random.seed(5945)

        # print("Test discover cell:")
        board = Board(rows=4, cols=4, mines=3)
        board.calculate()
        # view = BoardView(board)

        game = GameState(board)
        game.mark_cell(0, 0)
        game.open_cell(0, 1)
        game.discover_cell(0, 1)

        # view.render()

        self.assertEqual(list(map(lambda c: str(c), board.board[0:4])),
                         ['M', '1', '1', ' '], "First row should equal")
        self.assertEqual(list(map(lambda c: str(c), board.board[4:8])),
                         ['1', '1', '2', ' '], "Second row should equal")
        self.assertEqual(list(map(lambda c: str(c), board.board[8:12])),
                         [' ', ' ', ' ', ' '], "Third row should equal")
        self.assertEqual(list(map(lambda c: str(c), board.board[12:16])),
                         [' ', ' ', ' ', ' '], "Fourth row should equal")

        game.mark_cell(1, 3)
        game.mark_cell(2, 3)
        game.open_cell(1, 2)
        game.discover_cell(1, 2)

        self.assertEqual(list(map(lambda c: str(c), board.board[0:4])),
                         ['M', '1', '1', '1'], "First row should equal")
        self.assertEqual(list(map(lambda c: str(c), board.board[4:8])),
                         ['1', '1', '2', 'M'], "Second row should equal")
        self.assertEqual(list(map(lambda c: str(c), board.board[8:12])),
                         ['.', '.', '2', 'M'], "Third row should equal")
        self.assertEqual(list(map(lambda c: str(c), board.board[12:16])),
                         ['.', '.', '1', ' '], "Fourth row should equal")

        # view.render()
        # print()

    def test_is_game_over_with_explosion(self):
        random.seed(5945)

        # print("Test is game over:")

        board = Board(rows=4, cols=4, mines=3)
        board.calculate()
        # view = BoardView(board)
        game = GameState(board)
        game.open_cell(0, 0)

        # view.render()

        self.assertEqual(game.is_game_over(), True, "")
        self.assertEqual(game.explosed, True, "")

    def test_is_game_over(self):
        random.seed(5945)

        board = Board(rows=4, cols=4, mines=3)
        board.calculate()
        # view = BoardView(board)

        # view.render()

        game = GameState(board)
        game.open_cell(2, 0)

        game.mark_cell(1, 3)
        game.mark_cell(2, 3)
        game.discover_cell(1, 2)
        game.discover_cell(2, 2)

        # view.render()

        self.assertEqual(game.explosed, False, "Explosed must be false")
        self.assertEqual(game.is_game_over(), True, "Game over must be true")


if __name__ == '__main__':
    unittest.main()
