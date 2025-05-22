import data_service
import numpy as np
from tqdm import tqdm
from tfim_sk_infd.services import large_n_service
import sys

## ADJUST THESE
import sys

N = int(sys.argv[1])
seed_start = int(sys.argv[2])
seed_end = int(sys.argv[3])
batch_size = int(sys.argv[4])


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
