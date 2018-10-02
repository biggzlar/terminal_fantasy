import curses
import time
import random

import numpy as np

from objects import *

x = 0
y = 0

width = 20
height = 10

objects = []
space_tree = np.zeros([height * 2, width * 2])


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

    try:
        for i in range(10):
            report_progress("file_{0}.txt".format(i), i + 1)
            time.sleep(0.1)

        while True:
            c = stdscr.getch()
            current_position = (y, x)
            if c == ord('d'):
                x = (x + 1) % width
            if c == ord('a'):
                x = max((x - 1), 0)
            if c == ord('w'):
                y = max(y - 1, 0)
            if c == ord('s'):
                y = (y + 1) % height

            if collision(2+y, x, level=2):
                y, x = current_position

            if c == ord('+'):
                pos = (2 + random.randint(0, height - 1),
                       random.randint(0, width - 1))
                if not collision(*pos):
                    objects += [Plant(y=pos[0], x=pos[1],
                                      symbol="v", color=2, stdscr=stdscr, space_tree=space_tree)]
                    space_tree[pos] = 2

            if c == ord('q'):
                print(sorted(objects, key=lambda object: object.y))

            elif c == ord('c'):
                break

            # CLEAN SCREEN
            for i in range(10):
                stdscr.addstr(2 + i, 0, width * '.')
            
            # PROCESS + DRAW OBJECTS
            for obj in objects:
                obj.update(objects)

            # DRAW PLAYER
            stdscr.addstr(2+y, x, "+", curses.color_pair(1))
            stdscr.addstr(
                2, width + 2, "object count: {}".format(len(objects)))

    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()

