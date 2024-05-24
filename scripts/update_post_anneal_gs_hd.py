from database.models import InstancesN8
from tfim_sk_infd.services import ground_state_service
import data_service

N = 8


with data_service.get_session() as session:

    instances = (
        session.query(InstancesN8)
        .where(
            (InstancesN8.post_anneal_gs.is_not(None))
            & (InstancesN8.post_anneal_deg > 1)
        )
        .all()
    )

    for instance in instances:
        suppressed_gs = instance.post_anneal_gs

        instance.post_anneal_max_inter_gs_hd = ground_state_service.max_inter_gs_hd(
            suppressed_gs, N
        )

    session.commit()

    session.close()
