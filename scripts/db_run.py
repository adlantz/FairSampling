import numpy as np
from numpy import linalg
import tfim_sk_infd.services.ground_state_service as gss


import data_service
from database.models import InstancesN8, InstancesN12, InstancesN16
from tqdm import tqdm

N = 8

Instance = data_service.get_instance_class(N)


with data_service.get_session() as session:
    instances: List[Union[InstancesN8, InstancesN12, InstancesN16]] = (
        session.query(Instance).where(Instance.post_anneal_gs_probs.is_not(None)).all()
    )

    for instance in tqdm(instances):
        gs_probs = instance.post_anneal_gs_probs
        full_gs = instance.ground_states
        reduced_gs = instance.reduced_gs

        print(gs_probs)
        print(full_gs)
        print(reduced_gs)

        full_gs_probs = [0 for i in range(len(full_gs))]

        for i in range(len(reduced_gs)):
            full_gs_probs[full_gs.index(reduced_gs[i])] = full_gs_probs[
                full_gs.index((2**N) - 1 - reduced_gs[i])
            ] = (gs_probs[i] / 2)

        instance.full_post_anneal_gs_probs = full_gs_probs

    session.commit()
    session.close()
