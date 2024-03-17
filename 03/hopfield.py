import numpy as np
from copy import deepcopy
import pickle

class Pattern:
    def __init__(self, picture_matrix) -> None:
        self.picture_matrix = picture_matrix
        self.column_vector = np.where(picture_matrix == 0, -1, picture_matrix).flatten()
        self.transposed_column_vector = self.column_vector.reshape(-1, 1)
        self.weight_matrix = np.outer(self.column_vector, self.transposed_column_vector) - np.identity(len(self.column_vector)).astype(np.int32)
    
class HopfieldNetwork:
    def __init__(self, grid_size : int, stable_iterations : int) -> None:
        self.weights_matrix = np.zeros((grid_size **2, grid_size **2), np.int32)
        self.grid_size = grid_size
        self.patterns = []
        self.stable_iterations = stable_iterations

    def add_pattern(self, pattern : Pattern) -> bool:
        if self.contains_pattern(pattern):
            return False
       
        self.weights_matrix += pattern.weight_matrix
        self.patterns.append(deepcopy(pattern))

        return True

    def remove_pattern(self, pattern : Pattern) -> bool:
        for index, stored_pattern in enumerate(self.patterns):
            if np.array_equal(stored_pattern.picture_matrix, pattern.picture_matrix):
                self.weights_matrix -= pattern.weight_matrix
                del self.patterns[index]
                return True
            
        return False
    
    def contains_pattern(self, pattern : Pattern) -> bool:
        for stored_pattern in self.patterns:
            if np.array_equal(stored_pattern.picture_matrix, pattern.picture_matrix):
                return True
            
        return False
    
    def contains_pattern_vector(self, input_vector) -> bool:
        for stored_pattern in self.patterns:
            if np.array_equal(stored_pattern.column_vector, input_vector):
                return True
            
        return False

    def synchronous_recovery(self, input_pattern : Pattern) -> Pattern:
        result_vector = np.sign(np.dot(input_pattern.column_vector, self.weights_matrix))
        result_image = np.where(result_vector == -1, 0, result_vector).reshape((self.grid_size, self.grid_size))

        recovered_pattern = Pattern(result_image)

        return recovered_pattern if self.contains_pattern(recovered_pattern) else None

    def asynchronous_recovery(self, input_pattern : Pattern):
        input_vector = deepcopy(input_pattern.column_vector)

        prev_vector = None
        iterations = 0

        while True:
            for index in range(len(input_vector)):
                input_vector[index] = np.sign(np.dot(input_vector, self.weights_matrix[:, index]))

            iterations += 1

            if not np.array_equal(input_vector, prev_vector):
                iterations = 0

            prev_vector = deepcopy(input_vector)

            if iterations >= self.stable_iterations:
                break

        result_image = np.where(input_vector == -1, 0, input_vector).reshape((self.grid_size, self.grid_size))
        recovered_pattern = Pattern(result_image)

        return recovered_pattern if self.contains_pattern(recovered_pattern) else None
    
    def save_network(self, path : str) -> None:
        with open(path, 'wb') as file:
            pickle.dump(self, file)

    def load_network(path : str):
        with open(path, 'rb') as file:
            return pickle.load(file)
        
# network = HopfieldNetwork(2, 3)
# pattern = Pattern(np.array([[1, 0], [0, 1]]))
# network.add_pattern(pattern)
        
# recover = Pattern(np.array([[0, 1], [0, 1]]))
# pattern = network.asynchronous_recovery(recover)

# pass