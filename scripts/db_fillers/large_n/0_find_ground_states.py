import data_service

from database.models import LargeN
from tfim_sk_infd.services import large_n_service
import numpy as np
from tqdm import tqdm


N = 35

with data_service.get_session() as session:
    instances = []
    for seed in tqdm(range(0, 10)):
        gs, _ = large_n_service.generate_ground_states_bm(N, seed)
        instances.append(
            LargeN(size=N, seed=seed, ground_states=gs, degeneracy=len(gs))
        )
    session.bulk_save_objects(instances)
    session.commit()

    session.close()
