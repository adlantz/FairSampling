import numpy as np
from tfim_sk_infd.models.Jij import Jij
from scipy import sparse


def Jij_instance(N: int, seed: int) -> Jij:
    """Generates an random instance of couplings - bimodal - even ferro and anti-ferro"""

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
    return Jij(Jij_matrix)


def JZZ_SK(Jij: Jij) -> sparse.coo_matrix:
    """Builds matrices for infinite range zz interactions
    and returns each as a scipy.sparse.coo_matrix
    --JZZ = sum_{i,j} J_{ij}sigma^z_i sigma^z_j"""

    Jij_matrix = Jij.matrix
    N = Jij.N

    JZZ = np.zeros(2**N)
    shift_state = np.zeros(N, dtype=int)
    for b in range(2**N):
        state = 2 * np.array(list(bin(b)[2:].zfill(N))).astype(int) - 1
        for shift in range(1, N // 2 + 1):
            shift_state[shift:] = state[:-shift]
            shift_state[:shift] = state[-shift:]
            if (N % 2 == 0) and (shift == N // 2):
                JZZ[b] = JZZ[b] + 0.5 * np.dot(
                    Jij_matrix[shift - 1, :] * shift_state, state
                )
            else:
                JZZ[b] = JZZ[b] + np.dot(Jij_matrix[shift - 1, :] * shift_state, state)

    I = np.arange(2**N)

    return sparse.coo_matrix((JZZ, (I, I)), shape=(2**N, 2**N))


def compact_Jij_matrix(full_Jij: np.ndarray, N: int) -> Jij:
    compact_Jij = np.empty((N // 2, N))
    for j in range(N // 2):
        for i in range(N):
            compact_Jij[j][i] = full_Jij[i][(i - j + N - 1) % N]
    return Jij(compact_Jij)


def full_Jij_matrix(Jij: Jij) -> np.ndarray:
    """
    Turns Jij matrix from compact form built in Jij_instance to full form where J[i][j] is the bond between spins i and j
    """
    N = Jij.N
    compact_Jij = Jij.matrix
    full_Jij = np.zeros((N, N))
    for j in range(N // 2):
        for i in range(N):
            full_Jij[i][(i - j + N - 1) % N] = full_Jij[(i - j + N - 1) % N][i] = (
                compact_Jij[j][i]
            )
    return full_Jij


def get_toy_Jij(index: int) -> Jij:
    match index:
        case 1:
            return Jij(np.array([[0, 1, 1, 1, 1], [-1, -1, 1, 0, 1]]))
        case 2:
            return Jij(np.array([[1, 2, -2, 1, -2], [2, 1, 1, -1, 2]]))
        case 3:
            return Jij(
                np.array(
                    [[0, 0, 0, -1, 1, 1], [0, 0, 1, 1, 1, -1], [0, 0, -1, 0, 0, -1]]
                )
            )
        case 4:
            return Jij(np.array([[0, 1, -1, -1], [0, -1, 0, -1]]))
        case _:
            raise Exception(f"Toy model for index {index} does not exist")


def make_J_adj(Jij: Jij, N: int) -> np.ndarray:
    """
    Turns Jij matrix from form built in tfim.py to Jij adjacency matrix where J[i][j] is the bond between spins i and j
    """
    Jij_matrix = Jij.matrix
    J_adj = np.zeros((N, N))
    for j in range(N // 2):
        for i in range(N):
            J_adj[i][(i - j + N - 1) % N] = J_adj[(i - j + N - 1) % N][i] = Jij_matrix[
                j
            ][i]
    return J_adj
