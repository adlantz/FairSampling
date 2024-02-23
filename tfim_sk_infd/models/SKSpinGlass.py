import numpy as np
from scipy import sparse
import progressbar
from tfim_sk_infd.models.Jij import Jij
from tfim_sk_infd.models.IsingBasis import IsingBasis


class SKSpinGlass:
    Jij_matrix: np.ndarray  # Configuration of bonds
    N: int  # Number of spins
    M: int  # Number of possible configurations
    basis: IsingBasis  # Basis for classical Ising model
    JZZ: sparse.coo_matrix  # SK spin glass hamiltonian as a matrix
    Mx: sparse.coo_matrix  # Transverse field hamiltonian as a matrix

    def __init__(self, Jij: Jij):

        self.Jij_matrix = Jij.matrix
        self.N = Jij.N
        self.M = 2**self.N
        self.basis = IsingBasis(self.N)
        self.JZZ = self._JZZ_SK()
        self.Mx = self._build_Mx()

    def hamiltonian_at_h(self, h: float) -> sparse.coo_matrix:
        return -self.JZZ - h * self.Mx

    def _JZZ_SK(self) -> sparse.coo_matrix:
        """Builds matrices for infinite range zz interactions
        and returns each as a scipy.sparse.coo_matrix
        --JZZ = \sum_{i,j} J_{ij}\sigma^z_i \sigma^z_j"""
        print("Building JZZ...")
        JZZ = np.zeros(self.M)
        bar = progressbar.ProgressBar()
        shift_state = np.zeros(self.N, dtype=int)
        for b in bar(range(self.M)):
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
        print("Done.")
        I = np.arange(self.M)
        return sparse.coo_matrix((JZZ, (I, I)), shape=(self.M, self.M))

    def _build_Mx(self) -> sparse.coo_matrix:
        """Builds maxtrix of x-magnetization: \sum_i \sigma^x_i
        --returns scipy.sparse.coo_matrix"""

        print("Building Mx...")

        T = np.ones(self.M * self.N)
        I = np.ones(self.M * self.N)
        J = np.ones(self.M * self.N)

        bar = progressbar.ProgressBar()
        for ket in bar(range(self.M)):
            state = self.basis.state(ket)
            for i in range(self.N):
                self.basis.flip(state, i)
                bra = self.basis.index(state)
                self.basis.flip(state, i)
                I[ket * self.N + i] = ket
                J[ket * self.N + i] = bra

        print("Done.")

        return sparse.coo_matrix((T, (I, J)), shape=(self.M, self.M))
