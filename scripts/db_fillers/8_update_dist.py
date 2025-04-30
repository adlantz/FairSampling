import numpy as np
import tfim_sk_infd.services.ground_state_service as gss
import itertools as it


import data_service
from database.models import InstancesN8, InstancesN12, InstancesN16
from tqdm import tqdm


N = 16

Instance = data_service.get_instance_class(N)


with data_service.get_session() as session:

    instances = (
        session.query(Instance)
        .where(Instance.degeneracy > 2)
        .where(Instance.degeneracy <= 30)
        .where(Instance.dist_post_anneal.is_not(None))
        .all()
    )

    for instance in tqdm(instances):

        gs = instance.reduced_gs
        deg = instance.degeneracy // 2
        pa_gs_probs = np.array(instance.post_anneal_gs_probs)

        hamming_matrix = np.zeros((deg, deg))

        for i in range(deg):
            for j in range(i + 1, deg):
                hamming_matrix[i][j] = hamming_matrix[j][i] = (
                    gss.base_N_hamming_distance(gs[i], gs[j])
                )

        gs_indeces = [i for i in range(deg)]
        splittings = []
        for D in it.combinations(gs_indeces, deg // 2):
            A = tuple(gs_i for gs_i in gs_indeces if gs_i not in D)
            splittings.append((D, A))

        dist_list_fair = np.zeros(len(splittings))
        dist_list_pa = np.zeros(len(splittings))

        for i in range(len(splittings)):
            D = list(splittings[i][0])
            A = list(splittings[i][1])

            # if np.sum(pa_gs_probs[A]) < np.sum(pa_gs_probs[D]):
            #     A, D = D, A

            d_list_fair = np.zeros(len(D))
            d_list_pa = np.zeros(len(D))
            for j, gs_j in enumerate(D):
                d_list_fair[j] = np.min(hamming_matrix[gs_j, A]) * (1 / deg)
                d_list_pa[j] = np.min(hamming_matrix[gs_j, A]) * pa_gs_probs[gs_j]
            dist_list_fair[i] = 2 * np.sum(d_list_fair)
            dist_list_pa[i] = 2 * np.sum(d_list_pa)

        instance.dist_fair_sampling = max(dist_list_fair)
        # instance.dist_post_anneal = max(dist_list_pa)

        # TODO: find a way to do fair and PA at the same time (PA probability affects A D splitting)

    session.commit()
    session.close()
