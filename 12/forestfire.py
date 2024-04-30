import random

class ForestFire:
    EMPTY = 0
    TREE = 1
    FIRE = 2
    BURNT = 3

    def __init__(self, width : int, height : int, p : float, f : float, initial_p : float) -> None:
        self.width = width
        self.height = height
        self.p = p
        self.f = f

        self.grid = [[ForestFire.EMPTY for _ in range(width)] for _ in range(height)]

        for y in range(height):
            for x in range(width):
                if random.random() < initial_p:
                    self.grid[y][x] = ForestFire.TREE

    def is_fire_neighbour(self, x : int, y : int) -> bool:
        for dy in range(y - 1, y + 2):
            if dy < 0 or dy >= self.height:
                continue
            for dx in range(x - 1, x + 2):
                if (dy == y and x == x) or dx < 0 or dx >= self.width:
                    continue 
                if self.grid[dy][dx] == ForestFire.FIRE:
                    return True

        return False

    def update(self):
        new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]

                if cell == ForestFire.EMPTY:
                    if random.random() < self.p:
                        new_grid[y][x] = 1  
                elif cell == ForestFire.TREE: 
                    if self.is_fire_neighbour(x, y) or (random.random() < self.f):
                        new_grid[y][x] = ForestFire.FIRE
                    else:
                        new_grid[y][x] = ForestFire.TREE
                elif cell == ForestFire.FIRE:
                    new_grid[y][x] = ForestFire.BURNT
        self.grid = new_grid
