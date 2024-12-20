import numpy as np
from scipy import sparse
import networkx as nx
import qutip as qt
import matplotlib.pyplot as plt

import data_service

from tfim_sk_infd.services import jij_service, ground_state_service, qutip_service


# THINGS TO MODIFY

N = 8
seed_start = 0
seed_end = 10

## SCRIPT

out_obj = {}
for seed in range(seed_start, seed_end):
    # Get an instance and find ground state
    Jij = jij_service.Jij_instance(N, seed)
    JZZ = jij_service.JZZ_SK(Jij)
    gs_list = np.where(JZZ.diagonal() == JZZ.diagonal().max())[0]

    # Pull out half of the ground states and determine maximum hd
    reduced_gs, max_h_d = ground_state_service.maximal_half_clique(gs_list, N)

    # print(reduced_gs)

    gs_size = len(reduced_gs)

    if gs_size == 1:
        out_obj[seed] = {"reduced_gs": reduced_gs, "max_h_d": None, "supp_ratio": None}
        continue

    # Find ground state at low magnetic field strength
    Hp = qutip_service.spin_glass_hamiltonian(Jij, N)
    Ht = qutip_service.transverse_field_hamiltonian(N)

    h = 1e-2
    h_t = -Hp - h * Ht

    eigenvalues, eigenstates = h_t.eigenstates(eigvals=1)

    gs_probs = [
        2 * int(pa.real**2 + pa.imag**2)
        for pa in eigenstates[0].full().flatten()[reduced_gs]
    ]

    if abs(sum(gs_probs) - 1) > 1e-2:
        print(
            f"seed {seed} diagonalization fail. gs prob array sum {sum(gs_probs)}\n{gs_probs}"
        )
        continue

    suppression_ratio = 1 - (min(gs_probs) / max(gs_probs))

    out_obj[seed] = {
        # "full_gs": [int(gs) for gs in gs_list],
        # "reduced_gs": reduced_gs,
        "low_h_gs_probs": gs_probs,
        "max_h_d": max_h_d,
        "supp_ratio": suppression_ratio,
    }

data_service.save_obj("cat_data", str(N), f"{seed_start}_{seed_end}", out_obj)

print(out_obj)


# disc
# Hamming d
# variance of overlap dist
# mean of overlap dist
