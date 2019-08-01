from board import *
from game import *
from view import *
import curses

class Miner:
    def __init__(self, stdscr):
        self.board = Board(rows = 26, cols = 13, mines = 75)
        self.board.calculate()
        self.game = GameState(self.board)

        self.game_over = False
        self.board_pos = self.game.get_random_blank_cell()
        self.stdscr = stdscr

        self._init_colors()

        self.stdscr.clear()
        curses.curs_set(2)
        self.redraw()

    def _init_colors(self):
        curses.start_color()
        curses.use_default_colors()

        # closed: black foreground
        curses.init_pair(0, curses.COLOR_BLACK, curses.COLOR_BLACK)

        # opened blank
        curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # marked
        curses.init_pair(10, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(11, curses.COLOR_RED, curses.COLOR_WHITE)

        # opened nums
        curses.init_pair(1, 21,  curses.COLOR_WHITE)
        curses.init_pair(2, 76,  curses.COLOR_WHITE)
        curses.init_pair(3, 1,  curses.COLOR_WHITE)
        curses.init_pair(4, 99, curses.COLOR_WHITE)
        curses.init_pair(5, 11,  curses.COLOR_WHITE)
        curses.init_pair(6, 45,  curses.COLOR_WHITE)
        curses.init_pair(7, 6,   curses.COLOR_WHITE)
        curses.init_pair(8, 8,   curses.COLOR_WHITE)

    def redraw(self):
        self.stdscr.move(0, 0)

        for x in range(0, self.board.rows):
            for y in range(0, self.board.cols):
                pair = 0
                cell = self.board.cell(x, y)
                if cell.is_showed():
                    if cell.is_mined():
                        pair = 11
                    elif cell.is_valued():
                        pair = cell.number_of_mines()
                    else:
                        pair = 9
                elif cell.is_marked():
                    pair = 10

                self.stdscr.addstr(x, 2 * y, str(cell), curses.color_pair(pair))
                self.stdscr.addstr(x, 2 * y + 1, " ", curses.color_pair(pair))

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
