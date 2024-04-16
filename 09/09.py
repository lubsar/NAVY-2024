import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from copy import deepcopy

class Terrain:
    def __init__(self) -> None:
        self.points = np.zeros((2, 2))
        
    def subdivide(self, offset : float, clamp = 0.0) -> None:
        new_size = ((self.points.shape[0] - 1) * 2 + 1, (self.points.shape[1] - 1) * 2 + 1)

        new_points = np.zeros(new_size)

        for y in range(self.points.shape[0]):
            for x in range(self.points.shape[1]):
                 new_points[y * 2][x * 2] = self.points[y][x]

        for y in range(new_points.shape[0] // 2):
            yc = y * 2 + 1
            for x in range(new_points.shape[1] // 2):
                xc = x * 2 + 1
                if clamp == None:
                    a = new_points[yc - 1][xc] = (new_points[yc - 1][xc - 1] +  new_points[yc - 1][xc + 1]) / 2 + (offset if np.random.random() >= 0.5 else -offset)
                    b = new_points[yc + 1][xc] = (new_points[yc + 1][xc - 1] +  new_points[yc  + 1][xc + 1]) / 2 + (offset if np.random.random() >= 0.5 else -offset)
                    new_points[yc][xc - 1] = (new_points[yc - 1][xc -1] +  new_points[yc + 1][xc - 1]) / 2 + (offset if np.random.random() >= 0.5 else -offset)
                    new_points[yc][xc + 1] = (new_points[yc - 1][xc + 1] +  new_points[yc + 1][xc + 1]) / 2 + (offset if np.random.random() >= 0.5 else -offset)

                    new_points[yc][xc] = (a + b) / 2 + (offset if np.random.random() >= 0.5 else -offset)
                else:
                    a = new_points[yc - 1][xc] = max((new_points[yc - 1][xc - 1] +  new_points[yc - 1][xc + 1]) / 2 + (offset if np.random.random() >= 0.5 else -offset), clamp)
                    b = new_points[yc + 1][xc] = max((new_points[yc + 1][xc - 1] +  new_points[yc  + 1][xc + 1]) / 2 + (offset if np.random.random() >= 0.5 else -offset), clamp)
                    new_points[yc][xc - 1] = max((new_points[yc - 1][xc -1] +  new_points[yc + 1][xc - 1]) / 2 + (offset if np.random.random() >= 0.5 else -offset), clamp)
                    new_points[yc][xc + 1] = max((new_points[yc - 1][xc + 1] +  new_points[yc + 1][xc + 1]) / 2 + (offset if np.random.random() >= 0.5 else -offset), clamp)

                    new_points[yc][xc] = max((a + b) / 2 + (offset if np.random.random() >= 0.5 else -offset), clamp)

        self.points = new_points
        return new_points
    
def upsample(points, subdivision):
    points = deepcopy(points)

    for _ in range(subdivision):
        new_size = ((points.shape[0] - 1) * 2 + 1, (points.shape[1] - 1) * 2 + 1)

        new_points = np.zeros(new_size)

        for y in range(points.shape[0]):
            for x in range(points.shape[1]):
                    new_points[y * 2][x * 2] = points[y][x]

        for y in range(new_points.shape[0] // 2):
            yc = y * 2 + 1
            for x in range(new_points.shape[1] // 2):
                xc = x * 2 + 1
                
                a = new_points[yc - 1][xc] = (new_points[yc - 1][xc - 1] +  new_points[yc - 1][xc + 1]) / 2
                b = new_points[yc + 1][xc] = (new_points[yc + 1][xc - 1] +  new_points[yc  + 1][xc + 1]) / 2
                new_points[yc][xc - 1] = (new_points[yc - 1][xc -1] +  new_points[yc + 1][xc - 1]) / 2
                new_points[yc][xc + 1] = (new_points[yc - 1][xc + 1] +  new_points[yc + 1][xc + 1]) / 2

                new_points[yc][xc] = (a + b) / 2 

        points = new_points

    return points

def terain_animation(num_subdivisions):
    terrain = Terrain()

    heights = [upsample(terrain.points, num_subdivisions)]

    for x in range(1, num_subdivisions + 1):
        terrain.subdivide(1 / (x * 3))
        heights.append(upsample(terrain.points, num_subdivisions - x))

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    X = list(range(0, terrain.points.shape[1]))
    Y = list(range(0, terrain.points.shape[0]))

    X, Y = np.meshgrid(X, Y)
    
    mesh = ax.plot_surface(X, Y, heights[0], cmap='viridis')

    def update(frame):
        ax.clear()
        ax.set_xlim(0, terrain.points.shape[1])
        ax.set_ylim(0, terrain.points.shape[0])
        ax.set_zlim(np.min(heights), np.max(heights))

        ax.set_title("{0}. subdivision".format(frame % len(heights)))

        ax.plot_surface(X, Y, heights[frame % len(heights)], cmap='viridis')

    anim = FuncAnimation(fig, update, frames=len(heights), interval=500)

    plt.show()

terain_animation(3)
terain_animation(4)
terain_animation(8)
