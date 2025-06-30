import numpy as np
from typing import Optional


class Jij:
    def __init__(self, matrix: np.ndarray):
        self.matrix = matrix
        self.N = matrix.shape[1]

    @classmethod
    def generate(cls, N: int, seed: int = None) -> "Jij":
        """
        Generate a random Jij coupling matrix with bimodal distribution.
        Ensures equal number of ferromagnetic (+1) and antiferromagnetic (-1) bonds.
        """

        np.random.seed(seed)

        num_of_bonds = (N * (N - 1)) // 2
        if N % 4 == 0:
            a1 = [-1 for i in range(num_of_bonds // 2)]
        else:
            a1 = [-1 for i in range((num_of_bonds // 2) + 1)]
        a2 = [1 for i in range(num_of_bonds // 2)]
        a = list(np.random.permutation(a1 + a2))
        Jij_matrix = [a[(N * j) : N * (j + 1)] for j in range(N // 2)]
        if N % 2 == 0:
            Jij_matrix[(N // 2) - 1] += Jij_matrix[(N // 2) - 1]
        Jij_matrix = np.array(Jij_matrix)

        return cls(Jij_matrix)

    def full_Jij_matrix(self) -> np.ndarray:
        """
        Turns Jij matrix from compact form built in Jij_instance to full form where J[i][j] is the bond between spins i and j
        """
        N = self.N
        compact_Jij = self.matrix
        full_Jij = np.zeros((N, N))
        for j in range(N // 2):
            for i in range(N):
                full_Jij[i][(i - j + N - 1) % N] = full_Jij[(i - j + N - 1) % N][i] = (
                    compact_Jij[j][i]
                )
        return full_Jij

    def __repr__(self):
        return f"Jij(N={self.N})"

    def to_json(self) -> dict:
        """Convert to serializable JSON-like dict (e.g. for DB)"""
        return self.matrix.tolist()
