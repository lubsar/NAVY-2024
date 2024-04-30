import pygame
import sys
import time
from forestfire import ForestFire

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 2

GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

color_dict = {
    ForestFire.EMPTY : (0, 0, 0),
    ForestFire.TREE : (0, 255, 0),
    ForestFire.FIRE : (255, 0, 0),
    ForestFire.BURNT : (139, 69, 19)
}

p = 0.05
f = 0.001
initial_p = 0.5

ff = ForestFire(GRID_WIDTH, GRID_HEIGHT, p, f, initial_p)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Forest Fire")

def draw_grid(ff : ForestFire):
    for y in range(ff.height):
        for x in range(ff.width):
            color = color_dict[ff.grid[y][x]]
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ff.update()
    draw_grid(ff)
    pygame.display.flip()
    time.sleep(0.1) 

pygame.quit()
sys.exit()