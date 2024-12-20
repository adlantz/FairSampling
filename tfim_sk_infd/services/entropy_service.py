import itertools as it
import numpy as np
from scipy import linalg
from tfim_sk_infd.models.IsingBasis import IsingBasis


def get_bipartition_permutations(N: int) -> np.ndarray:
    bp_perms = []

    if N % 2 == 0:
        combos = list(it.combinations([i for i in range(N)], N // 2))
        num_bps = len(combos) // 2
        for i in range(num_bps):
            bp_perms.append(list(combos[i] + combos[-1 - i]))

    else:
        combos1 = list(it.combinations([i for i in range(N)], N // 2))
        combos2 = list(it.combinations([i for i in range(N)], N // 2 + 1))
        num_bps = len(combos1)
        for i in range(num_bps):
            bp_perms.append(list(combos1[i] + combos2[-i - 1]))

    return np.array(bp_perms)


def get_entanglement_entropy_information(basis: IsingBasis, psi0: np.ndarray):
    bp_perms = get_bipartition_permutations(basis.N)

    svn = np.zeros(len(bp_perms))
    s_eng = np.zeros((len(bp_perms), 2 ** (basis.N // 2)))
    for i, P in enumerate(bp_perms):
        A = P[0 : (basis.N // 2)]
        B = P[(basis.N // 2) : basis.N]
        S = get_svd(basis, A, B, psi0)

        svn[i] = entropy(S)
        s_eng[i] = np.sort(0 - 2 * np.log(S))

    return svn, s_eng


def get_svd_reduced(
    ground_states: np.ndarray, A: np.ndarray, B: np.ndarray, gs_amps: np.ndarray, N: int
):

    gs_bin = np.array(
        [np.array([int(bit) for bit in bin(g)[2:].zfill(N)]) for g in ground_states]
    )

    a_space = np.array(
        list({int("".join(state[A].astype(str)), 2) for state in gs_bin})
    )
    b_space = np.array(
        list({int("".join(state[B].astype(str)), 2) for state in gs_bin})
    )
    psiMat = np.zeros([len(a_space), len(b_space)])
    for i, state in enumerate(gs_bin):
        a_state = int("".join(state[A].astype(str)), 2)
        b_state = int("".join(state[B].astype(str)), 2)
        a_index = np.where(a_space == a_state)[0][0]
        b_index = np.where(b_space == b_state)[0][0]
        psiMat[a_index, b_index] = gs_amps[i]
    return linalg.svd(psiMat, compute_uv=False)


def get_svd(
    basis: IsingBasis,
    A: np.ndarray,
    B: np.ndarray,
    v: np.ndarray,
) -> np.ndarray:
    """Compute the singular value decomposition of vector v
    ---A, B are the lists of sites in each bipartition"""

    a_basis = IsingBasis(len(A))
    b_basis = IsingBasis(len(B))

    # Build psi matrix
    psiMat = np.zeros([a_basis.M, b_basis.M])
    for index in range(basis.M):
        state = basis.state(index)
        a_state = state[A]
        b_state = state[B]
        a_index = a_basis.index(a_state)
        b_index = b_basis.index(b_state)
        psiMat[a_index, b_index] = v[index]

    # Perform SVD
    return linalg.svd(psiMat, compute_uv=False)


def entropy(S: np.ndarray) -> int:
    return -np.sum(S**2 * np.log(S**2))


def entropy_zeros(S: np.ndarray) -> int:
    return round(-np.sum(np.where(S == 0, 0, S**2 * np.log(S**2))), 10)


def disconnectivity(gs_amps: np.ndarray, ground_states: np.ndarray, N: int):

    disconnectivity = 1
    min_delta_m = 0.1
    full_spin_list = [i for i in range(N)]
    ent_cache = {tuple(full_spin_list): 0, (): 0}
    spin_set = set(full_spin_list)

    for bp_size in range(2, N + 1):
        for bp in list(it.combinations(range(N), bp_size)):
            if bp in ent_cache:
                S_bp = ent_cache[bp]
            else:
                bp_A = np.array(bp)
                bp_B = np.array(list(spin_set - set(bp)))
                S_bp = round(
                    entropy_zeros(
                        get_svd_reduced(ground_states, bp_A, bp_B, gs_amps, N)
                    ),
                    5,
                )
                ent_cache[tuple(bp_A)] = ent_cache[tuple(bp_B)] = S_bp

            min_S_sub_bp = 100000
            sub_spin_set = set(bp)
            for sub_bp_size in range(1, bp_size):
                for sub_bp_n in list(it.combinations(list(bp), sub_bp_size)):

                    # Partition n
                    if sub_bp_n in ent_cache:
                        S_bp_n = ent_cache[tuple(sub_bp_n)]
                    else:
                        bp_A_n = np.array(sub_bp_n)
                        bp_B_n = np.array(list(spin_set - set(sub_bp_n)))
                        S_bp_n = round(
                            entropy_zeros(
                                get_svd_reduced(
                                    ground_states, bp_A_n, bp_B_n, gs_amps, N
                                )
                            ),
                            5,
                        )
                        ent_cache[tuple(bp_A_n)] = ent_cache[tuple(bp_B_n)] = S_bp_n

                    # Partition M-n
                    sub_bp_Mn = sub_spin_set - set(sub_bp_n)
                    if tuple(sub_bp_Mn) in ent_cache:
                        S_bp_Mn = ent_cache[tuple(sub_bp_Mn)]
                    else:
                        bp_A_Mn = np.array(list(sub_bp_Mn))
                        bp_B_Mn = np.array(list(spin_set - sub_bp_Mn))
                        S_bp_Mn = round(
                            entropy_zeros(
                                get_svd_reduced(
                                    ground_states, bp_A_Mn, bp_B_Mn, gs_amps, N
                                )
                            ),
                            5,
                        )
                        ent_cache[tuple(bp_A_Mn)] = ent_cache[tuple(bp_B_Mn)] = S_bp_Mn

                    if S_bp_n + S_bp_Mn < min_S_sub_bp:
                        min_S_sub_bp = S_bp_n + S_bp_Mn

            delta_m = S_bp / min_S_sub_bp if min_S_sub_bp != 0 else 1

            if delta_m <= min_delta_m:
                disconnectivity = bp_size

    return disconnectivity
