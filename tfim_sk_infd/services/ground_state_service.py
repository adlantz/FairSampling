import numpy as np
import networkx as nx
from typing import Optional


def maximal_half_clique(gs_list: list[int], N: int) -> tuple[list[int], Optional[int]]:

    gs_size = len(gs_list)

    if gs_size == 2:
        # trivial case, return one gs randomly and None for max_hd
        return [gs_list[0]], None

    maximal_clique_len = 0
    h_d_cap = N / 2
    while maximal_clique_len < gs_size / 2:

        Aij, max_h_d = build_capped_hamming_Aij(gs_list, gs_size, h_d_cap, N)

        maximal_clique = max(nx.find_cliques(nx.Graph(Aij)), key=len)
        maximal_clique_len = len(maximal_clique)

        h_d_cap += 1

    return [gs_list[i] for i in maximal_clique], max_h_d


def build_capped_hamming_Aij(gs_list: list, gs_size: int, h_d_cap: int, N: int):
    max_h_d = 0
    Aij = np.zeros((gs_size, gs_size))
    for i in range(gs_size):
        for j in range(i + 1, gs_size):
            h_d = base_N_hamming_distance(gs_list[i], gs_list[j], N)
            if h_d <= h_d_cap:
                Aij[i][j] = Aij[j][i] = np.exp(-h_d)
                if h_d > max_h_d:
                    max_h_d = h_d
    return Aij, max_h_d


def base_N_hamming_distance(i: int, j: int, N: int) -> int:
    arr_i = np.array([int(s) for s in bin(i)[2:].zfill(N)])
    arr_j = np.array([int(s) for s in bin(j)[2:].zfill(N)])
    return int(np.sum(arr_i != arr_j))


def max_inter_gs_hd(gs_list: list[int], N: int) -> int:
    gs_size = len(gs_list)
    max_h_d = 0
    for i in range(gs_size):
        for j in range(i + 1, gs_size):
            h_d = base_N_hamming_distance(gs_list[i], gs_list[j], N)
            if h_d > max_h_d:
                max_h_d = h_d
    return max_h_d


def overlap_distribution_old(gs_list: list[int], N: int) -> list[float]:
    overlap_dist = []
    for i in range(len(gs_list)):
        for j in range(i, len(gs_list)):
            h_d = base_N_hamming_distance(gs_list[i], gs_list[j], N)
            overlap_dist.append((N - (2 * h_d)) / N)

    return overlap_dist


def overlap_distribution(gs_list: list[int], N: int) -> np.ndarray:
    gs_size = len(gs_list)
    overlap_dist = np.zeros((gs_size * (gs_size + 1)) // 2)
    for i in range(gs_size):
        for j in range(i, gs_size):
            h_d = base_N_hamming_distance(gs_list[i], gs_list[j], N)
            overlap_dist[i + j] = (N - (2 * h_d)) / N

    return overlap_dist
