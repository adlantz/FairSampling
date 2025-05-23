from tfim_sk_infd.services import ground_state_service
import data_service
from tqdm import tqdm


from database.models import InstancesN8, InstancesN12, InstancesN16

import sys

N = int(sys.argv[1])

Instance = data_service.get_instance_class(N)


with data_service.get_session() as session:

    instances = session.query(Instance).where(Instance.reduced_gs.is_(None)).all()

    for instance in tqdm(instances):
        reduced_gs, max_h_d = ground_state_service.maximal_half_clique(
            instance.ground_states, N
        )
        instance.reduced_gs = reduced_gs
        instance.max_inter_gs_hd = max_h_d

    session.commit()

    session.close()
