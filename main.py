from board import *
from game import *
from view import *
import curses

class Miner:
    def __init__(self, stdscr):
        self.board = Board(rows = 20, cols = 10, mines = 35)
        self.board.calculate()
        self.game = GameState(self.board)

        self.game_over = False
        self.board_pos = (0, 0)
        self.cursor_pos = (0, 0)
        self.stdscr = stdscr

        self.stdscr.clear()
        curses.curs_set(2)
        self.redraw()

    def redraw(self):
        self.stdscr.move(0, 0)

        for x in range(0, self.board.rows):
            row = " ".join([str(self.board.cell(x, y)) for y in range(0, self.board.cols)])
            self.stdscr.addstr(x, 0, row, curses.A_BOLD)

        self.move_cursor()
        self.stdscr.refresh()

    def move_cursor(self):
        self.stdscr.move(self.board_pos[0], self.board_pos[1] * 2)

    def run(self):
        while True:
            key = self.stdscr.getch()

            if key == ord('q'):
                break
            elif key == curses.KEY_RIGHT:
                if self.board_pos[1] == self.board.cols - 1:
                    self.board_pos = (self.board_pos[0], 0)
                else:
                    self.board_pos = (self.board_pos[0], self.board_pos[1] + 1)
                self.move_cursor()
            elif key == curses.KEY_LEFT:
                if self.board_pos[1] == 0:
                    self.board_pos = (self.board_pos[0], self.board.cols - 1)
                else:
                    self.board_pos = (self.board_pos[0], self.board_pos[1] - 1)
                self.move_cursor()
            elif key == curses.KEY_DOWN:
                if self.board_pos[0] == self.board.rows - 1:
                    self.board_pos = (0, self.board_pos[1])
                else:
                    self.board_pos = (self.board_pos[0] + 1, self.board_pos[1])
                self.move_cursor()
            elif key == curses.KEY_UP:
                if self.board_pos[0] == 0:
                    self.board_pos = (self.board.rows - 1, self.board_pos[1])
                else:
                    self.board_pos = (self.board_pos[0] - 1, self.board_pos[1])
                self.move_cursor()
            elif key == ord(' '):
                self.game.open_cell(self.board_pos[0], self.board_pos[1])
                self.redraw()
                if self.game.is_game_over():
                    self.game_over = True
                    break
            elif key == ord('m'):
                self.game.mark_cell(self.board_pos[0], self.board_pos[1])
                self.redraw()
            elif key == ord('d'):
                self.game.discover_cell(self.board_pos[0], self.board_pos[1])
                self.redraw()
                if self.game.is_game_over():
                    self.game_over = True
                    break

        if self.game_over:
            self.stdscr.getch()

def main(stdscr):
    miner = Miner(stdscr)
    miner.run()

curses.wrapper(main)
