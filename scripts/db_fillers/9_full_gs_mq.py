import numpy as np
from numpy import linalg
import tfim_sk_infd.services.ground_state_service as gss


import data_service
from database.models import InstancesN8, InstancesN12, InstancesN16
from tqdm import tqdm
from typing import List, Union

N = 16

Instance = data_service.get_instance_class(N)


with data_service.get_session() as session:
    instances: List[Union[InstancesN8, InstancesN12, InstancesN16]] = (
        session.query(Instance)
        .where(Instance.degeneracy > 2)
        .where(Instance.full_gs_post_anneal_od_variance.is_(None))
        .all()
    )
    od_bins = np.array([((2 * i) / N) - 1 for i in range(N + 1)])
    for instance in tqdm(instances):

        gs_array = instance.ground_states

        deg = instance.degeneracy

        H = np.zeros((deg, deg))
        P = np.zeros((deg, deg))
        for i in range(deg):
            for j in range(i + 1, deg):
                H[i][j] = H[j][i] = gss.base_N_hamming_distance(
                    gs_array[i], gs_array[j]
                )
                P[i][j] = instance.full_post_anneal_gs_probs[j]
                P[j][i] = instance.full_post_anneal_gs_probs[i]

        instance.full_gs_qfi_post_anneal = max(
            4 * (np.sum(H * H * P, axis=1) - np.sum(H * P, axis=1) ** 2)
        ) / (N**2)
        instance.full_gs_qfi_fair_sampling = max(
            (4 / deg)
            * ((linalg.norm(H, axis=1)) ** 2 - (1 / deg) * (np.sum(H, axis=1)) ** 2)
        ) / (N**2)

        overlap_dist = gss.overlap_distribution_fair(instance.ground_states, N)
        mean = np.sum(od_bins * overlap_dist)
        instance.full_gs_od_variance = np.sum(overlap_dist * (od_bins - mean) ** 2)
        suppressed_overlap_dist = gss.overlap_distribution_weighted(
            instance.ground_states, instance.full_post_anneal_gs_probs, N
        )
        mean = np.sum(od_bins * suppressed_overlap_dist)
        instance.full_gs_post_anneal_od_variance = np.sum(
            suppressed_overlap_dist * (od_bins - mean) ** 2
        )

    session.commit()
    session.close()
