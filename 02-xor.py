import numpy as np

class NeuralNetwork:
    def __init__(self, input_size : int, num_hidden_neurons : int, num_output_neurons : int, activation, activation_derivative) -> None:
        self.hidden_weights = np.random.random(size=(num_hidden_neurons, input_size))
        self.hidden_biases = np.random.random(size=(1, num_hidden_neurons))
        self.output_weights = np.random.random(size=(num_hidden_neurons, num_output_neurons))
        self.output_biases = np.random.random(size=(1, num_output_neurons))
        self.activation = activation
        self.activation_derivative = activation_derivative
    
    # calculate output of network for specific data point
    def output(self, inputs) -> float:
        hidden_output = self.activation(np.dot(inputs, self.hidden_weights) + self.hidden_biases)
        output = self.activation(np.dot(hidden_output, self.output_weights) + self.output_biases)

        return (hidden_output, output)

    # train network on all training data in one epoch
    def train(self, X, Y, learning_rate, num_epochs) -> None:
        assert(len(X) == len(Y))

        # train whole dataset num epoch times
        for _ in range(num_epochs): 
            # train of each record
            for data_index in range(len(X)):
                x = X[data_index]
                y = Y[data_index]

                # calculate output and its error based on current weights and biases
                hidden_output, output = self.output(x)
                error = y - output

                # calculate changes to output and hidden layer weights and biases
                delta_output = error * self.activation_derivative(output)
                delta_hidden = delta_output * self.output_weights.T * self.activation_derivative(hidden_output)

                # recalculate weights and biases using training record error
                self.output_weights += delta_output * hidden_output.T * learning_rate
                self.hidden_weights += delta_hidden * x * learning_rate

                self.output_biases += learning_rate * delta_output
                self.hidden_biases += learning_rate * delta_hidden

    def predict(self, X):
        return [self.output(x)[1] for x in X]

def sigmoid (x):
    return 1/(1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

X_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
Y_train = np.array([[0], [1], [1], [0]])

network = NeuralNetwork(2, 2, 1, sigmoid, sigmoid_derivative)

num_epochs = 10000
learning_rate = 0.1

network.train(X_train, Y_train, learning_rate, num_epochs)

print(np.round(network.predict(X_train)))