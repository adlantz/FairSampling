import numpy as np
from numpy import linalg
import tfim_sk_infd.services.ground_state_service as gss


import data_service
from database.models import InstancesN8, InstancesN12, InstancesN16
from tqdm import tqdm

N = 16

Instance = data_service.get_instance_class(N)


with data_service.get_session() as session:
    instances: list[InstancesN8 | InstancesN12 | InstancesN16] = (
        session.query(Instance).where(Instance.degeneracy > 2).all()
    )

    for instance in tqdm(instances):

        gs_array = instance.reduced_gs

        deg = instance.degeneracy // 2

        H = np.zeros((deg, deg))
        P = np.zeros((deg, deg))
        for i in range(deg):
            for j in range(i + 1, deg):
                H[i][j] = H[j][i] = gss.base_N_hamming_distance(
                    gs_array[i], gs_array[j]
                )
                P[i][j] = instance.post_anneal_gs_probs[j]
                P[j][i] = instance.post_anneal_gs_probs[i]

        instance.qfi_post_anneal = max(
            4 * (np.sum(H * H * P, axis=1) - np.sum(H * P, axis=1) ** 2)
        ) / (N**2)
        instance.qfi_fair_sampling = max(
            (4 / deg)
            * ((linalg.norm(H, axis=1)) ** 2 - (1 / deg) * (np.sum(H, axis=1)) ** 2)
        ) / (N**2)

    session.commit()
    session.close()
