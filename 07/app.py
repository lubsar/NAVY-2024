import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import random 
import copy

from common.visualization import *

model1_transformations = [
    (np.transpose(np.array([0.00, 0.00, 0.01, 0.00, 0.26, 0.00, 0.00, 0.00, 0.05]).reshape((3, 3))), np.array([0.0, 0.0, 0.0])),
    (np.transpose(np.array([0.20, -0.26, -0.01, 0.23, 0.22, -0.07, 0.07, 0.00, 0.24]).reshape((3, 3))), np.array([0.0, 0.8, 0.0])),
    (np.transpose(np.array([-0.25, 0.28, 0.01, 0.26, 0.24, -0.07, 0.07, 0.00, 0.24]).reshape((3, 3))), np.array([0.0, 0.22, 0.0])),
    (np.transpose(np.array([0.85, 0.04, -0.01, -0.04, 0.85, 0.09, 0.00, 0.08, 0.84]).reshape((3, 3))), np.array([0.0, 0.80, 0.0]))
]

model2_transformations = [
    (np.transpose(np.array([0.05, 0.00, 0.00, 0.00, 0.60, 0.00, 0.00, 0.00, 0.05]).reshape((3, 3))), np.array([0.0, 0.0, 0.0])),
    (np.transpose(np.array([0.45, -0.22, 0.22, 0.22, 0.45, 0.22, -0.22, 0.22, -0.45]).reshape((3, 3))), np.array([0.0, 1.0, 0.0])),
    (np.transpose(np.array([-0.45, 0.22, -0.22, 0.22, 0.45, 0.22, 0.22, -0.22, 0.45]).reshape((3, 3))), np.array([0.0, 1.25, 0.0])),
    (np.transpose(np.array([0.49, -0.08, 0.08, 0.08, 0.49, 0.08, 0.08, -0.08, 0.49]).reshape((3, 3))), np.array([0.0, 2.0, 0.0]))
]

def createPoints(start_point, transformations, iterations : int) -> list[np.ndarray]:
    points = np.array([start_point])
    point = np.array([start_point])

    for i in range(iterations):
        current_transformation = random.choice(transformations)
        matrix = current_transformation[0]
        translation = current_transformation[1]
        
        point = np.add(np.dot(point, matrix), translation)
        points = np.concatenate((points, point), axis=0)

    return points

model1 = createPoints([0.0, 0.0, 0.0], model1_transformations, 10000)

visual = Visualisation3D(False)
visual.fig.canvas.manager.set_window_title("Model 1")
visual.plotPointsAnimation(model1)
visual.show()

model2 = createPoints([0.0, 0.0, 0.0], model2_transformations, 10000)

visual = Visualisation3D(False)
visual.fig.canvas.manager.set_window_title("Model 2")
visual.plotPointsAnimation(model2)
visual.show()

