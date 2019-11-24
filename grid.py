import random
import itertools
import numpy


class Grid:
    def __init__(self, size=(10, 10)):
        self.nil = "-"
        self.size = size
        self.grid = [" "] * size[0]
        self.grid = [[self.nil] * size[1] for x in self.grid]
        self.objects = {}

    def add(self, a, x, y):
        if self.get(x, y) != self.nil:
            return False
        self.grid[x][y] = a[0]
        self.objects[a] = (x, y)
        return True

    def add_rand(self, a):
        if len(self.objects) >= self.size[0] * self.size[1]:
            return False
        points = [
            (x, y)
            for x in range(self.size[0])
            for y in range(self.size[1])
            if self.grid[x][y] == self.nil
        ]
        return self.add(a, *random.choice(points))

    def draw(self):
        s = ""
        for x in self.grid:
            for y in x:
                s += y + " "
            s += "\n"
        return s

    def move(self, a, dx, dy):
        # Enumerate moves
        traj = (1, 0)
        if dx < 0:
            traj = (-1, 0)
            dx = -dx
        x = [traj for _ in range(dx)]

        traj = (0, 1)
        if dy < 0:
            traj = (0, -1)
            dy = -dy
        y = [traj for _ in range(dy)]

        moves = list(
            filter(
                lambda x: x is not None,
                itertools.chain.from_iterable(itertools.zip_longest(x, y)),
            )
        )

        # Walk through moves
        for delta in moves:
            pos = self.get_pos(a)
            if not pos:
                return False
            newpos = tuple(numpy.add(pos, delta))
            if self.get(*newpos) != self.nil:
                moves = [x for x in moves if x != delta]
                continue
            self[pos] = self.nil
            self[newpos] = a[0]
            self.objects[a] = newpos

        return True

    def get(self, x, y):
        if x >= self.size[0] or x < 0 or y >= self.size[1] or y < 0:
            return False
        return self.grid[x][y]

    def get_pos(self, a):
        if a not in self.objects:
            return False
        return self.objects[a]

    def __setitem__(self, tup, val):
        self.grid[tup[0]][tup[1]] = val
