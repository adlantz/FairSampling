import numpy as np
from scipy import sparse
import progressbar
import numpy as np
from scipy.sparse import linalg as spla
from core.Jij import Jij
from core.IsingBasis import IsingBasis


class QuantumSpinGlass:
    Jij_matrix: np.ndarray  # Configuration of bonds
    N: int  # Number of spins
    M: int  # Number of possible configurations
    basis: IsingBasis  # Basis for classical Ising model
    JZZ: sparse.coo_matrix  # SK spin glass hamiltonian as a matrix
    Mx: sparse.coo_matrix  # Transverse field hamiltonian as a matrix
    classical_ground_states: list

    def __init__(self, Jij: Jij, classical_ground_states: list):

        self.Jij_matrix = Jij.matrix
        self.N = Jij.N
        self.M = 2**self.N
        self.basis = IsingBasis(self.N)
        self.JZZ = self._JZZ_SK()
        self.Mx = self._build_Mx()
        self.U = self._build_U()
        self.classical_ground_states = classical_ground_states

    def hamiltonian_at_h(self, h: float) -> sparse.coo_matrix:
        return -self.JZZ - h * self.Mx

    def _JZZ_SK(self) -> sparse.coo_matrix:
        """Builds matrices for infinite range zz interactions
        and returns each as a scipy.sparse.coo_matrix
        --JZZ = sum_{i,j} J_{ij}sigma^z_i sigma^z_j"""
        JZZ = np.zeros(self.M)
        shift_state = np.zeros(self.N, dtype=int)
        for b in range(self.M):
            state = self.basis.spin_state(b)
            for shift in range(1, self.N // 2 + 1):
                shift_state[shift:] = state[:-shift]
                shift_state[:shift] = state[-shift:]
                if (self.N % 2 == 0) and (shift == self.N // 2):
                    JZZ[b] = JZZ[b] + 0.5 * np.dot(
                        self.Jij_matrix[shift - 1, :] * shift_state, state
                    )
                else:
                    JZZ[b] = JZZ[b] + np.dot(
                        self.Jij_matrix[shift - 1, :] * shift_state, state
                    )
        I = np.arange(self.M)
        return sparse.coo_matrix((JZZ, (I, I)), shape=(self.M, self.M))

    def _build_Mx(self) -> sparse.coo_matrix:
        """Builds maxtrix of x-magnetization: sum_i sigma^x_i
        --returns scipy.sparse.coo_matrix"""

        T = np.ones(self.M * self.N)
        I = np.ones(self.M * self.N)
        J = np.ones(self.M * self.N)

        for ket in range(self.M):
            state = self.basis.state(ket)
            for i in range(self.N):
                self.basis.flip(state, i)
                bra = self.basis.index(state)
                self.basis.flip(state, i)
                I[ket * self.N + i] = ket
                J[ket * self.N + i] = bra

        return sparse.coo_matrix((T, (I, J)), shape=(self.M, self.M))

    def _build_U(self):
        rows = []
        cols = []
        data = []

        for i in range(self.M):
            val = 1.0 if i < self.M // 2 else -1.0
            rows.append(i)
            cols.append(i)
            data.append(val)

            rows.append(i)
            cols.append(self.M - i - 1)
            data.append(1.0)

        U = sparse.coo_matrix((data, (rows, cols)), shape=(self.M, self.M))
        U /= np.sqrt(2)
        return U

    def get_post_anneal_info(self):

        h_array = []
        fidelities = []
        e_gaps = []
        total_gs_probs = []

        psi0_1q = None
        diag_failure = False
        i = 0
        h = 1e-1
        while i < 10:
            H = self.hamiltonian_at_h(h)

            UHU = self.U @ H @ self.U.T

            UHU1q = UHU[0 : self.M // 2, 0 : self.M // 2]
            try:
                E, v = spla.eigsh(UHU1q, k=2, which="SA", v0=psi0_1q)

                sort_order = np.argsort(E)
                E = E[sort_order]
                v = v[:, sort_order]
                old_psi0_1q = psi0_1q
                psi0_1q = v[:, 0]
                psi0_complete = self.U @ (np.append(psi0_1q, np.zeros(self.M // 2)))

                h_array.append(h)
                fidelities.append(
                    np.abs(np.vdot(psi0_1q, old_psi0_1q))
                    if old_psi0_1q is not None
                    else 1
                )
                e_gaps.append(E[1] - E[0])
                total_gs_probs.append(
                    np.sum(psi0_complete[self.classical_ground_states] ** 2)
                )
            except:
                diag_failure = True

            if diag_failure or (
                i > 1
                and total_gs_probs[i] > 0.99
                and fidelities[i] > 0.99
                and fidelities[i - 1] > 0.99
            ):
                break

            h /= 2 if i % 2 == 0 else 5
            i += 1

        if i > 1:
            gs_probs = psi0_complete[self.classical_ground_states] ** 2
            return (
                (psi0_complete[self.classical_ground_states] ** 2).tolist(),
                round(1 - (np.min(gs_probs) / np.max(gs_probs)), 6),
                h_array,
                fidelities,
                e_gaps,
                diag_failure,
            )

        else:
            return None, None, None, None, None, diag_failure
