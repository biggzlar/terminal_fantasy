import os
import time
import curses
import random

import numpy as np

from objects import *

x = 0
y = 0

WIDTH = 20
HEIGHT = 10

objects = []
space_tree = np.zeros([HEIGHT * 2, WIDTH * 2])


def collision(y, x, level=1):
    return space_tree[y, x] == level

def report_progress(filename, progress):
    """progress: 0-10"""
    stdscr.addstr(0, 0, "roading resources: {0}".format(filename))
    stdscr.addstr(1, 0, "Total progress: [{1:10}] {0}%".format(
        progress * 10, "#" * progress), curses.A_STANDOUT)
    stdscr.refresh()

if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    curses.start_color()
    # (id, foreground, background)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)

    try:
        # for i in range(10):
        #     report_progress("file_{0}.txt".format(i), i + 1)
        #     time.sleep(0.1)

        while True:
            rows, cols = os.popen('stty size', 'r').read().split()
            y_offset = (int(rows) - HEIGHT) // 2
            x_offset = (int(cols) -  WIDTH) // 2

            stdscr.addstr(2, WIDTH + 40, ('y_offset ' + str(y_offset)))
            stdscr.addstr(3, WIDTH + 40, ('x_offset ' + str(x_offset)))

            c = stdscr.getch()
            current_position = (y, x)
            if c == ord('d'):
                x = (x + 1) % WIDTH
            if c == ord('a'):
                x = max(x - 1, 0)
            if c == ord('w'):
                y = max(y - 1, 0)
            if c == ord('s'):
                y = (y + 1) % HEIGHT

            if collision(y, x, level=2):
                y, x = current_position

            if c == ord('+'):
                pos = (random.randint(0, HEIGHT - 1),
                            random.randint(0, WIDTH - 1))

                if not collision(*pos):
                    objects += [Plant(y=pos[0], x=pos[1],
                                      stdscr=stdscr, space_tree=space_tree)]
                    
                    space_tree[pos] = 2

            if c == ord('q'):
                # print(sorted(objects, key=lambda object: object.y))
                objects += [Monkey(y=8, x=8, stdscr=stdscr, space_tree=space_tree)]

            elif c == ord('c'):
                break

            # CLEAN SCREEN
            for i in range(10):
                stdscr.addstr(y_offset + i, x_offset + 0, WIDTH * '.', curses.A_DIM)

            # PROCESS + DRAW OBJECTS
            for obj in objects:
                obj.update(objects, y_offset, x_offset)

            # DRAW PLAYER
            stdscr.addstr(y_offset + y, x_offset + x, "+", curses.color_pair(1))
            stdscr.addstr(
                y_offset,x_offset + WIDTH + 2, "object count: {}".format(len(objects)))
            stdscr.refresh()

    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()

