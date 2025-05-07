import data_service
import numpy as np
from tqdm import tqdm
from tfim_sk_infd.services import large_n_service

## ADJUST THESE
N = 16
seed_start = 2050
seed_end = 5000
batch_size = 100


# SCRIPT

Instance = data_service.get_instance_class(N)

with data_service.get_session() as session:
    instances = []
    for seed in tqdm(range(seed_start, seed_end)):

        gs, Jij = large_n_service.generate_ground_states_bm(N, seed)
        instances.append(
            Instance(seed=seed, Jij_matrix=Jij.matrix.tolist(), ground_states=gs)
        )

        if (seed + 1) % batch_size == 0:
            session.bulk_save_objects(instances)
            session.commit()
            instances = []
    session.bulk_save_objects(instances)
    session.commit()

    session.close()
