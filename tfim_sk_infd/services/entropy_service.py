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

    # Build psi matrix |psi><psi|
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
