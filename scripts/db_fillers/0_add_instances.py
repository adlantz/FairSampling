import data_service
import numpy as np
from typing import Type
from tfim_sk_infd.services import jij_service

## ADJUST THESE
N = 12
seed_start = 0
seed_end = 1000
batch_size = 100


# SCRIPT

Instance = data_service.get_instance_class(N)

with data_service.get_session() as session:
    instances = []
    for seed in range(seed_start, seed_end):

        Jij = jij_service.Jij_instance(N, seed)
        JZZ = jij_service.JZZ_SK(Jij)
        gs = np.where(JZZ.diagonal() == JZZ.diagonal().max())[0]
        instances.append(
            Instance(
                seed=seed, Jij_matrix=Jij.matrix.tolist(), ground_states=gs.tolist()
            )
        )

        if (seed + 1) % batch_size == 0:
            session.bulk_save_objects(instances)
            session.commit()
            instances = []
    session.bulk_save_objects(instances)
    session.commit()

    session.close()
