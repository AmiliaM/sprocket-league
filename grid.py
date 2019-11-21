import random


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
        print(points)
        return self.add(a, *random.choice(points))

    def draw(self):
        s = ""
        for x in self.grid:
            for y in x:
                s += y + " "
            s += "\n"
        return s

    def move(self, a, dx, dy):
        pos = self.get_pos(a)
        if not pos:
            return False
        x, y = pos
        self.grid[x][y] = self.nil

        x += dx
        y += dy
        if x >= self.size[0]:
            x = self.size[0] - 1
        elif x < 0:
            x = 0

        if y >= self.size[0]:
            y = self.size[0] - 1
        elif y < 0:
            y = 0

        self.grid[x][y] = a[0]
        self.objects[a] = (x, y)

        return

    def get(self, x, y):
        if x >= self.size[0] or x < 0 or y >= self.size[1] or y < 0:
            return False
        return self.grid[x][y]

    def get_pos(self, a):
        if a not in self.objects:
            return False
        return self.objects[a]
