import qutip as qt
import numpy as np

from tfim_sk_infd.models.Jij import Jij
from tfim_sk_infd.services import jij_service


def spin_glass_hamiltonian(Jij: Jij, N: int) -> qt.Qobj:
    J_adj = jij_service.make_J_adj(Jij, N)
    si = qt.qeye(2)
    sz = qt.sigmaz()
    Hp = 0
    for i in range(len(J_adj)):
        for j in range(i, len(J_adj[i])):

            sigma_i = [si if k != i else sz for k in range(N)]
            sigma_j = [si if l != j else sz for l in range(N)]

            Hp += J_adj[i][j] * qt.tensor(sigma_i) * qt.tensor(sigma_j)

    return Hp


def transverse_field_hamiltonian(N: int) -> qt.Qobj:
    si = qt.qeye(2)
    sx = qt.sigmax()

    Ht = 0
    for i in range(N):
        sigma_x = [si if k != i else sx for k in range(N)]
        Ht += qt.tensor(sigma_x)

    return Ht


def quantum_anneal(
    Hp: qt.Qobj, Ht: qt.Qobj, N: int, annealing_time: int, steps: int
) -> list[float]:

    taulist = np.linspace(0, annealing_time, steps)

    # Initialize in equal superposition
    psi_list = [(1 / np.sqrt(2)) * (qt.basis(2, 0) + qt.basis(2, 1)) for n in range(N)]
    psi0 = qt.tensor(psi_list)

    # the time-dependent hamiltonian in list-function format
    args = {"t_max": annealing_time}
    h_t = [
        [-Ht, lambda t, args: (annealing_time - t) / annealing_time],
        [-Hp, lambda t, args: t / annealing_time],
    ]

    # transform Hamiltonian to QobjEvo
    h_t = qt.QobjEvo(h_t, args=args)

    # anneal and return final ground state probabilities
    res = qt.sesolve(h_t, psi0, taulist, [], args)
    final_state = [(x.real**2 + x.imag**2)[0] for x in res.states[-1].full()]

    return final_state
