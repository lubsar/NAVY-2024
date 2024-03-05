import numpy as np
import matplotlib.pyplot as plt

class Perceptron:
    def __init__(self, num_weights : int, activation) -> None:
        self.weights = np.random.random(num_weights)
        self.bias = np.random.random()
        self.activation = activation
    
    # calculate output of neuron for specific data point
    def output(self, inputs) -> float:
        assert(len(inputs) == len(self.weights))

        return self.activation(np.dot(inputs, self.weights) + self.bias)

    # recalculate weight based on related input, error and learning rate
    def recalculateWeight(self, input : float, weight : float, error : float, learning_rate : float) -> float:
        return weight + error * input * learning_rate

    # recalculate perceptron bias based on error and learning rate of training record
    def recalculateBias(self, error : float, learning_rate : float) -> float:
        self.bias = self.bias + error * learning_rate

    # train perceptron on all training data in one epoch
    def train(self, X, Y, learning_rate) -> None:
        assert(len(X) == len(Y))

        # train of each record
        for data_index in range(len(X)):
            x = X[data_index]
            y = Y[data_index]

            # calculate output and its error based on current perceptron weights and biases
            output = self.output(x)
            error = y - output

            # recalculate weights using training record error
            for weight_index in range(len(self.weights)):
                self.weights[weight_index] = self.recalculateWeight(x[weight_index], self.weights[weight_index], error, learning_rate)
            
            # recalculate perceptron bias using training record error 
            self.recalculateBias(error, learning_rate)

    # calcualte perceptron output for each (testing) record
    def predict(self, X):
        return np.apply_along_axis(self.output, 1, X)

### Ploting function
def plotData(X, Y):
    x_values = X[:, 0]
    y_values = X[:, 1]
    colors = ['blue', 'black', 'red'] 

    point_colors = [colors[int(y + 1)] for y in Y] # black = on line, red = above line, blue = bellow line

    plt.scatter(x_values, y_values, c=point_colors)
    plt.plot([lower_bound, upper_bound], [separation_line(lower_bound), separation_line(upper_bound)], c="black")

    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')

    plt.legend()
    plt.show()

### Data generation
def separation_line(x):
    return 3 * x + 2

def on_separation_line(coords):
    x = coords[0]
    y = coords[1]

    line_y = 3 * x + 2

    return 1 if y > line_y else -1 if y < line_y else 0 

# generate random points, make sure at least 1/3 of points is on line, so each class is present in training data
def generateData(count : int, lower_bound : float, upper_bound : float):
    num_random_points = 2 * count // 3
    num_on_line_points = count - num_random_points

    number_range = abs(upper_bound - lower_bound)

    #random points
    X_random = np.random.random((num_random_points, 2)) * number_range + lower_bound 

    # on line points
    X_on_line_x = np.random.random(num_on_line_points) * number_range + lower_bound 
    X_on_line_y = np.apply_along_axis(separation_line, 0, X_on_line_x)
    X_on_line = np.vstack((X_on_line_x, X_on_line_y)).T

    # combine and shuffle data so points whih are on line are distributed among other points
    X = np.vstack((X_random, X_on_line))
    np.random.shuffle(X)
  
    #X = np.random.random((count, 2)) * number_range + lower_bound
    Y = np.apply_along_axis(on_separation_line, 1, X)

    return (X, Y)

### Testing 
perceptron = Perceptron(2, np.sign) #initialization with 2 dimensions

# problem space and data 
lower_bound, upper_bound = -30, 30
num_training_records = 1000 # training set with 10x testing records
num_testing_records = 100

X_train, Y_train = generateData(num_training_records, lower_bound, upper_bound)
X_test, Y_test = generateData(num_testing_records, lower_bound, upper_bound)

#training one epoch and prediction 
perceptron.train(X_train, Y_train, 0.1)
Y_predict = perceptron.predict(X_test)

# visualisation
plotData(X_test, Y_test)
pass