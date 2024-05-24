import numpy as np

from database.models import InstancesN8
from tfim_sk_infd.services import ground_state_service
import data_service

N = 8


with data_service.get_session() as session:

    instances = session.query(InstancesN8).where(InstancesN8.degeneracy > 2).all()

    for instance in instances:

        overlap_dist = ground_state_service.overlap_distribution(instance.reduced_gs, N)
        instance.overlap_dist = overlap_dist.tolist()
        instance.od_mean = round(np.mean(overlap_dist), 5)
        instance.od_variance = round(np.var(overlap_dist), 5)

    session.commit()

    session.close()
