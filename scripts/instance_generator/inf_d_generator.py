from tfim_sk_infd.services import jij_service
import data_service
import numpy as np
import json


N = 8

for seed in range(100, 1000):

    Jij = jij_service.Jij_instance(N, seed)
    JZZ = jij_service.JZZ_SK(Jij)
    gs = np.where(JZZ.diagonal() == JZZ.diagonal().max())[0]
    degeneracy = len(gs)
    instance_info = {
        "Jij_matrix": json.dumps(Jij.matrix.tolist()),
        "gs": json.dumps(gs.tolist()),
    }

    data_service.save_obj(
        "instances", f"inf_d/{N}/gs_{degeneracy}", str(seed), instance_info
    )
