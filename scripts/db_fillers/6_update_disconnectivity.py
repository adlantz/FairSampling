import itertools as it
import qutip as qt
import numpy as np
import tfim_sk_infd.services.entropy_service as tfe
from typing import Optional


import data_service
from database.models import InstancesN8, InstancesN12, InstancesN16
from tqdm import tqdm

fair_discs = []
pa_discs = []

N = 16

Instance = data_service.get_instance_class(N)


with data_service.get_session() as session:
    instances: list[InstancesN8 | InstancesN12 | InstancesN16] = (
        session.query(Instance)
        .where(Instance.degeneracy > 2)
        .where(Instance.disc_fair_sampling.is_(None))
        .all()
    )

    for instance in tqdm(instances):

        fair_sampling_gs_amps = np.array(
            [np.sqrt(1 / (instance.degeneracy // 2)) for _ in instance.reduced_gs]
        )
        instance.disc_fair_sampling = tfe.disconnectivity(
            fair_sampling_gs_amps,
            np.array(instance.reduced_gs),
            N,
        )
        post_anneal_gs_amps = np.sqrt(np.array(instance.post_anneal_gs_probs))
        post_anneal_gs_amps /= np.linalg.norm(post_anneal_gs_amps)
        instance.disc_post_anneal = tfe.disconnectivity(
            post_anneal_gs_amps,
            np.array(instance.reduced_gs),
            N,
        )

    session.commit()
    session.close()
