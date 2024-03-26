import numpy as np
from copy import deepcopy
import pickle
import random

class EnvironmentMatrix:
    def __init__(self, environment, score_dict : dict) -> None:
        self.environment_dimension = len(environment)
        self.environment = environment
        self.score_dict = score_dict
        matrix_dimension = self.environment_dimension ** 2
        self.target_states = []

        self.matrix = np.full(shape=(matrix_dimension, matrix_dimension), fill_value=-1)

        for row in range(self.environment_dimension):
            for column in range(self.environment_dimension):
                matrix_index = row * self.environment_dimension + column

                if (row - 1) >= 0:
                    top = (row - 1) * self.environment_dimension + column
                    self.matrix[matrix_index][top] = score_dict[environment[row - 1][column]]
                    
                if (row + 1) < self.environment_dimension:
                    bottom = (row + 1) * self.environment_dimension + column
                    self.matrix[matrix_index][bottom] = score_dict[environment[row + 1][column]]

                if (column - 1) >= 0:
                    left = matrix_index - 1
                    self.matrix[matrix_index][left] = score_dict[environment[row][column - 1]]

                if (column + 1) < self.environment_dimension:
                    right = matrix_index + 1
                    self.matrix[matrix_index][right] = score_dict[environment[row][column + 1]]

                if environment[row][column] == 'cheese':
                    self.matrix[matrix_index][matrix_index] = score_dict[environment[row][column]]
                    self.target_states.append(matrix_index)

class QLearning:
    def __init__(self, environment : EnvironmentMatrix) -> None:
        self.q_matrix = np.zeros(environment.matrix.shape)
        self.environment  = environment

    def train(self, starting_location : tuple[int, int], num_epochs : int, learning_rate : float, maximize_next_state = False):
        for epoch in range(num_epochs):
            agent_start = np.random.random_integers(0, self.environment.environment_dimension - 1, 2)
            while self.environment.score_dict[self.environment.environment[agent_start[0]][agent_start[1]]] < 0:
                agent_start = np.random.random_integers(0, self.environment.environment_dimension - 1, 2)

            current_state = agent_start[0] * self.environment.environment_dimension + agent_start[1] 
            print("epoch {} / {}".format(epoch + 1, num_epochs))

            while True :
                if maximize_next_state:
                    next_states = np.argwhere(self.environment.matrix[current_state] >= np.amax(self.environment.matrix[current_state])).flatten()
                else:
                    next_states = np.argwhere(self.environment.matrix[current_state] >= 0).flatten()

                next_state = random.choice(next_states)
                new_score = self.environment.matrix[current_state][next_state] + learning_rate * np.amax(self.q_matrix[next_state])

                self.q_matrix[current_state][next_state] = new_score

                if current_state in self.environment.target_states:
                    break

                current_state = next_state

    def get_steps(self, start : tuple[int, int], max_length = 1000) -> list[tuple[int, int]]:
        current_state = start[0] * self.environment.environment_dimension + start[1] 
        
        steps = [start]

        length = 0
        while current_state not in self.environment.target_states and length < max_length:
            next_states = np.argwhere(self.q_matrix[current_state] >= np.amax(self.q_matrix[current_state])).flatten()
            next_state = random.choice(next_states)
            
            value = self.q_matrix[current_state][next_state]

            if value == 0:
                return None
            
            steps.append((next_state // self.environment.environment_dimension, next_state % self.environment.environment_dimension))
            length += 1

            current_state = next_state
            

        return steps