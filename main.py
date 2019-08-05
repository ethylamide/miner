# coding: utf-8

import argparse
import curses

from board import *
from game import *
from view import *

class MineSweeper:
    def __init__(self, stdscr, rows, cols, mines):
        self.board = Board(rows, cols, mines)
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

        # opened nums
        curses.init_pair(1, 21,  curses.COLOR_WHITE)
        curses.init_pair(2, 76,  curses.COLOR_WHITE)
        curses.init_pair(3, 1,  curses.COLOR_WHITE)
        curses.init_pair(4, 99, curses.COLOR_WHITE)
        curses.init_pair(5, 11,  curses.COLOR_WHITE)
        curses.init_pair(6, 45,  curses.COLOR_WHITE)
        curses.init_pair(7, 6,   curses.COLOR_WHITE)
        curses.init_pair(8, 8,   curses.COLOR_WHITE)

        # opened blank
        curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # marked
        curses.init_pair(10, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(11, curses.COLOR_RED, curses.COLOR_WHITE)

        # lines
        curses.init_pair(12, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def redraw(self):
        self.stdscr.move(0, 0)

        # for x in range(0, self.board.rows):

        tl = 0
        tr = 1
        bl = 2
        br = 3

        corners = ['┌', '┐', '└', '┘' ]

        hor = 0
        ver = 1
        lines = ['─', '│']

        self.stdscr.addstr(0, 0, corners[tl])
        for x in range(1, 2 * (self.board.cols + 1)):
            self.stdscr.addstr(0, x, lines[hor], curses.color_pair(12))
        self.stdscr.addstr(0, 2 * self.board.cols + 2, corners[tr])

        for x in range(0, self.board.rows):
            self.stdscr.addstr(x + 1, 0, lines[ver], curses.color_pair(12))
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

                self.stdscr.addstr(x + 1, 2 * (y + 1), str(cell), curses.color_pair(pair))
                self.stdscr.addstr(x + 1, 2 * (y + 1) + 1, " ", curses.color_pair(pair))
            self.stdscr.addstr(x + 1, 2 * self.board.cols + 2, lines[ver], curses.color_pair(12))

        self.stdscr.addstr(self.board.rows + 1, 0, corners[bl])
        self.stdscr.addstr(self.board.rows + 1, 1, lines[hor])
        for x in range(0, self.board.cols):
            self.stdscr.addstr(self.board.rows + 1, 2 * x + 2, lines[hor], curses.color_pair(12))
            self.stdscr.addstr(self.board.rows + 1, 2 * x + 3, lines[hor], curses.color_pair(12))
        self.stdscr.addstr(self.board.rows + 1, 2 * self.board.cols + 2, corners[br])

        self.move_cursor()
        self.stdscr.refresh()

    def move_cursor(self):
        self.stdscr.move(self.board_pos[0] + 1, 2 * (self.board_pos[1] + 1))

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
    complexity = {
        'easy': (12, 6, 10),
        'medium': (20, 10, 35),
        'hard': (26, 13, 75)
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('--complexity', help='game complexity: easy|medium|hard')
    args = parser.parse_args()

    c = complexity['medium']

    if args.complexity in complexity:
        c = complexity[args.complexity]

    minesweeper = MineSweeper(stdscr, c[0], c[1], c[2])
    minesweeper.run()

curses.wrapper(main)
