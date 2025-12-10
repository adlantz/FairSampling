# import numpy as np
# from numpy import linalg
# import tfim_sk_infd.services.ground_state_service as gss


# import data_service
# from database.models import InstancesN8, InstancesN12, InstancesN16
# from tqdm import tqdm

# N = 16

# Instance = data_service.get_instance_class(N)


# with data_service.get_session() as session:
#     instances = session.query(Instance).where(Instance.seed > 2000).all()

#     for instance in tqdm(instances):
#         print(instance.seed)

#     gs_probs = instance.post_anneal_gs_probs
#     full_gs = instance.ground_states
#     reduced_gs = instance.reduced_gs

#     print(gs_probs)
#     print(full_gs)
#     print(reduced_gs)

#     full_gs_probs = [0 for i in range(len(full_gs))]

#     for i in range(len(reduced_gs)):
#         full_gs_probs[full_gs.index(reduced_gs[i])] = full_gs_probs[
#             full_gs.index((2**N) - 1 - reduced_gs[i])
#         ] = (gs_probs[i] / 2)

#     instance.full_post_anneal_gs_probs = full_gs_probs

# session.commit()
# session.close()


from tfim_sk_infd.services import large_n_service

import sys

N = int(sys.argv[1])
seed = 1

gs, Jij = large_n_service.generate_ground_states_bm(N, seed)


# print(Jij.matrix)
print(Jij.matrix.size)

print(gs)
