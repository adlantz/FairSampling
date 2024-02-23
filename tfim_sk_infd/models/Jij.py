import numpy as np


class Jij:
    matrix: np.ndarray  # Matrix representation of Jij bonds
    N: int  # Number of spins in the system

    def __init__(self, matrix: np.ndarray):
        self.matrix = matrix
        self.N = matrix.shape[1]
