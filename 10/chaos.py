import numpy as np
import matplotlib.pyplot as plt
import sklearn.neural_network._multilayer_perceptron as mlp


def logistic_function(a : float, x : float) -> float:
    return a * x * (1.0 - x)

num_iterations = 100
num_a_subdivision = 1000 # subdivison


a_values = np.linspace(0.0, 4.0, num_a_subdivision)

Ys = []

init_x = np.random.random()
for a_index, a in enumerate(a_values):
    Y = np.zeros(num_iterations)
    x = init_x
    
    for _ in range(100):
        x = logistic_function(a, x)

    for iter in range(num_iterations):
        x = logistic_function(a, x)
        Y[iter] = x
    
    Ys.append(Y)
    plt.scatter([a] * num_iterations, Y, 0.01, c='blue')

plt.show()

neural_network = mlp.MLPRegressor(hidden_layer_sizes=(1,100,100), max_iter=2000)
neural_network.fit(a_values.reshape(-1,1), Ys)


for a_index, a in enumerate(a_values):
    Y = neural_network.predict(np.array([a]).reshape(-1,1))
    
    Ys.append(Y)
    plt.scatter([a] * num_iterations, Y, 0.01, c='blue')

plt.show()


