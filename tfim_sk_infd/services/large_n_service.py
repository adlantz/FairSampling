from tfim_sk_infd.services import jij_service
import numpy as np
from tfim_sk_infd.models.branchboundV11 import BB
import string
from tfim_sk_infd.models.Jij import Jij
import time


def biqMac(Jij: Jij):
    """
    efficiently calculates the ground states of a given Jij instance
    """
    N = Jij.N
    arr = jij_service.full_Jij_matrix(Jij)
    Q2 = np.array(arr)
    P2 = np.zeros(N)
    R2 = 0
    for i in range(N):
        for j in range(N):
            P2[i] += Q2[i][j]
            R2 += Q2[i][j]
    solver = BB(-2 * Q2, 2 * P2, -0.5 * R2)
    return solver.solve()


def binary_to_decimal(array):
    """
    Converts an array of spins to its corresponding decimal value
    """
    array = array.translate(str.maketrans("", "", string.punctuation))
    array = array.replace(" ", "")

    binary = int(array, 2)

    return binary


def generate_ground_states_bm(N: int, seed: int):
    Jij = jij_service.Jij_instance(N, seed=seed)
    bm = biqMac(Jij)
    return [binary_to_decimal(b) for b in bm], Jij
