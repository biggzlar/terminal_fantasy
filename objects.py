import curses
import random


class Base:

    def __init__(self, x, y, symbol, color):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.color = color

    def update(self, objects, y_offset, x_offset):
        self.stdscr.addstr(self.y + y_offset, self.x + x_offset, self.symbol,
                           curses.color_pair(self.color))


class Plant(Base):

    def __init__(self, stdscr, space_tree, x=0, y=0, symbol='v', color=2, species=0):
        Base.__init__(self, x, y, symbol, color)
        self.species = species
        self.stdscr = stdscr
        self.space_tree = space_tree

    def update(self, objects, y_offset, x_offset):
        Base.update(self, objects, y_offset, x_offset)
        if random.random() < 0.1:
            pos = (max(0, self.y + random.choice([-1, 0, 1])), max(0, self.x + random.choice([-1, 0, 1])))
            
            try:
                if not self.space_tree[pos] > 0:
                    objects += [Fruit(stdscr=self.stdscr, y=pos[0], x=pos[1])]
                    self.space_tree[pos] = 1
            except:
                pass


class Fruit(Base):

    def __init__(self, stdscr, x=0, y=0, symbol='*', color=3, kind=0):
        Base.__init__(self, x, y, symbol, color)
        self.kind = kind
        self.stdscr = stdscr


class Monkey(Base):

    def __init__(self, stdscr, space_tree, x=0, y=0, symbol='@', color=4):
        Base.__init__(self, x, y, symbol, color)
        self.stdscr = stdscr
        self.space_tree = space_tree

    def update(self, objects, y_offset, x_offset):
        actions = ['up', 'down', 'left', 'right', 'none']
        action = random.choice(actions)

        current_position = (self.y, self.x)

        if action=='up':
            self.y = max(0, self.y - 1)
        if action=='down':
            self.y = (self.y + 1) % 10 # height
        if action=='left':
            self.x = max(0, self.x - 1)
        if action=='right':
            self.x = (self.x + 1) % 20 # width

        if self.space_tree[self.y, self.x] == 2:
            self.y, self.x = current_position

        Base.update(self, objects, y_offset, x_offset)

