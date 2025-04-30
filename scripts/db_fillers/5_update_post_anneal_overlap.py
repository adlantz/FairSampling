import numpy as np
from database.models import InstancesN8, InstancesN12, InstancesN16
from tfim_sk_infd.services import ground_state_service
import data_service
from tqdm import tqdm

N = 16


Instance = data_service.get_instance_class(N)

with data_service.get_session() as session:

    instances: list[InstancesN8 | InstancesN12 | InstancesN16] = (
        session.query(Instance)
        .where(Instance.post_anneal_gs_probs.is_not(None))
        .where(Instance.post_anneal_overlap_dist.is_(None))
        .all()
    )
    od_bins = np.array([((2 * i) / N) - 1 for i in range(N + 1)])
    for instance in tqdm(instances):
        suppressed_overlap_dist = ground_state_service.overlap_distribution_weighted(
            instance.reduced_gs, instance.post_anneal_gs_probs, N
        )
        instance.post_anneal_overlap_dist = suppressed_overlap_dist.tolist()
        instance.post_anneal_od_mean = mean = np.sum(od_bins * suppressed_overlap_dist)
        instance.post_anneal_od_variance = np.sum(
            suppressed_overlap_dist * (od_bins - mean) ** 2
        )

    print(f"updated {len(instances)} columns")

    session.commit()

    session.close()
