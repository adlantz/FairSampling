import numpy as np

from database.models import InstancesN8
from sqlalchemy import update, func
from tfim_sk_infd.services import ground_state_service, qutip_service
from tfim_sk_infd.models.Jij import Jij
import data_service


N = 8

with data_service.get_session() as session:

    instances = (
        session.query(InstancesN8)
        .where(
            (InstancesN8.post_anneal_supp_ratio > 0.9)
            & (InstancesN8.post_anneal_gs.is_(None))
        )
        .all()
    )

    for instance in instances:

        gs_probs = instance.post_anneal_gs_probs
        max_probability = max(gs_probs)

        # suppressed gs is the indeces of the ground states have the maximum probability in the quantum gs
        suppressed_gs = [
            instance.reduced_gs[i]
            for i, gsp in enumerate(gs_probs)
            if abs(max_probability - gsp) < 1e-2
        ]

        instance.post_anneal_gs = suppressed_gs
        instance.post_anneal_deg = len(suppressed_gs)

        if len(suppressed_gs) > 1:
            suppressed_overlap_dist = ground_state_service.overlap_distribution(
                suppressed_gs, N
            )
            instance.post_anneal_overlap_dist = suppressed_overlap_dist.tolist()
            instance.post_anneal_od_mean = round(np.mean(suppressed_overlap_dist), 5)
            instance.post_anneal_od_variance = round(np.var(suppressed_overlap_dist), 5)

    print(f"updated {len(instances)} columns")

    session.commit()

    session.close()
