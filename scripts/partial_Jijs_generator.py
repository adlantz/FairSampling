from tfim_sk_infd.services import jij_service
import data_service
import numpy as np
import json
import itertools as it


N = 8
num_broken_bonds = 7
bond_list = [list(c) for c in it.combinations([i for i in range(N)], 2)]
# print(bond_list)


for seed in range(0, 1000):

    Jij = jij_service.Jij_instance(N, seed)
    full_Jij = jij_service.full_Jij_matrix(Jij)
    broken_bonds = np.random.choice(np.arange(N), size=num_broken_bonds, replace=False)
    for broken_bond in broken_bonds:
        spin_i, spin_j = bond_list[broken_bond]
        full_Jij[spin_i][spin_j] = full_Jij[spin_j][spin_i] = 0

    Jij = jij_service.compact_Jij_matrix(full_Jij, N)

    JZZ = jij_service.JZZ_SK(Jij)
    gs = np.where(JZZ.diagonal() == JZZ.diagonal().max())[0]
    degeneracy = len(gs)
    instance_info = {
        "Jij_matrix": json.dumps(Jij.matrix.tolist()),
        "gs": json.dumps(gs.tolist()),
        "broken_bonds": json.dumps([bond_list[b] for b in broken_bonds]),
    }

    data_service.save_obj(
        "instances",
        f"partial/{N}/broken_{num_broken_bonds}/gs_{degeneracy}",
        str(seed),
        instance_info,
    )
