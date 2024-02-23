import numpy as np


class IsingBasis:
    """Basis for the Hilbert space of an Ising Model"""

    def __init__(self, N: int):
        self.N = N  # Number of spins
        self.M = 2**N  # Size of basis

    def state(self, index):
        """Returns the state associated with index"""
        return np.array(list(bin(index)[2:].zfill(self.N))).astype(int)

    def spin_state(self, index):
        """Returns the spin state associated with index"""
        return 2 * self.state(index) - 1

    def index(self, state):
        """Returns the index associated with state"""
        return int("".join(state.astype(str)), 2)

    def flip(self, state, i):
        """Flips ith spin in state"""
        state[i] = (state[i] + 1) % 2
