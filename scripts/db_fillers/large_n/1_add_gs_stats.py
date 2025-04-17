import data_service

from database.models import LargeN
from tfim_sk_infd.services import large_n_service, ground_state_service
import numpy as np

from tqdm import tqdm


N = 20

with data_service.get_session() as session:

    instances: list[LargeN] = (
        session.query(LargeN)
        .where(LargeN.degeneracy > 2)
        .where(LargeN.reduced_gs.is_(None))
        .all()
    )
    od_bins = np.array([((2 * i) / N) - 1 for i in range(N + 1)])
    for instance in tqdm(instances):
        reduced_gs, _ = ground_state_service.maximal_half_clique(
            instance.ground_states, N
        )
        overlap_dist = ground_state_service.overlap_distribution_fair(reduced_gs, N)
        overlap_dist = overlap_dist.tolist()
        od_mean = np.sum(od_bins * overlap_dist)
        od_variance = np.sum(overlap_dist * (od_bins - od_mean) ** 2)

        gs_array = reduced_gs
        deg = instance.degeneracy // 2
        H = np.zeros((deg, deg))
        for i in range(deg):
            for j in range(i + 1, deg):
                H[i][j] = H[j][i] = ground_state_service.base_N_hamming_distance(
                    gs_array[i], gs_array[j]
                )

        instance.reduced_gs = reduced_gs
        instance.overlap_dist = overlap_dist
        instance.od_mean = od_mean
        instance.od_variance = od_variance
        instance.n_eff = max(
            (4 / deg)
            * ((np.linalg.norm(H, axis=1)) ** 2 - (1 / deg) * (np.sum(H, axis=1)) ** 2)
        ) / (N**2)

    session.commit()
    session.close()
