import numpy as np

from database.models import InstancesN8, InstancesN12, InstancesN16
from tfim_sk_infd.services import ground_state_service
import data_service
from tqdm import tqdm


import sys

N = int(sys.argv[1])
Instance = data_service.get_instance_class(N)

with data_service.get_session() as session:

    instances = (
        session.query(Instance)
        .where(Instance.degeneracy > 2)
        .where(Instance.overlap_dist.is_(None))
        .all()
    )
    od_bins = np.array([((2 * i) / N) - 1 for i in range(N + 1)])
    for instance in tqdm(instances):

        overlap_dist = ground_state_service.overlap_distribution_fair(
            instance.reduced_gs, N
        )
        instance.overlap_dist = overlap_dist.tolist()
        instance.od_mean = mean = np.sum(od_bins * overlap_dist)
        instance.od_variance = np.sum(overlap_dist * (od_bins - mean) ** 2)

    session.commit()

    session.close()
