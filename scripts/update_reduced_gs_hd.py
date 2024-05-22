from database.models import InstancesN8
from tfim_sk_infd.services import ground_state_service
import data_service

N = 8


with data_service.get_session() as session:

    instances = session.query(InstancesN8).all()

    for instance in instances:
        reduced_gs, max_h_d = ground_state_service.maximal_half_clique(
            instance.ground_states, N
        )
        instance.reduced_gs = reduced_gs
        instance.max_inter_gs_hd = max_h_d

    session.commit()

    session.close()
