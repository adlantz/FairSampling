import numpy as np

from database.models import InstancesN8, InstancesN12, InstancesN16
from tfim_sk_infd.services import qutip_service
from tfim_sk_infd.models.Jij import Jij
from tfim_sk_infd.models.SKSpinGlass import SKSpinGlass
import data_service
from tqdm import tqdm
from scipy import sparse
from scipy.sparse import linalg as spla

N = 16
M = 2**N

# Spin inversion operator
U = np.zeros((M, M))
for i in range(M):
    U[i][i] = 1 if i < (M) // 2 else -1
    U[i][-i - 1] = 1
U /= np.sqrt(2)
U = sparse.coo_matrix(U)


Instance = data_service.get_instance_class(N)


with data_service.get_session() as session:

    instances: list[InstancesN8 | InstancesN12 | InstancesN16] = (
        session.query(Instance)
        .where(Instance.degeneracy > 2)
        .where(Instance.diag_run_failure.is_(None))
        .all()
    )

    for instance in tqdm(instances):

        Jij_obj = Jij(np.array(instance.Jij_matrix))
        SG = SKSpinGlass(Jij_obj)

        h_array = []
        fidelities = []
        e_gaps = []
        total_gs_probs = []

        psi0_1q = None
        diag_failure = False
        i = 0
        h = 1e-1
        while i < 10:
            H = SG.hamiltonian_at_h(h)

            UHU = U @ H @ U.T

            UHU1q = UHU[0 : SG.M // 2, 0 : SG.M // 2]
            try:
                E, v = spla.eigsh(UHU1q, k=2, which="SA", v0=psi0_1q)

                sort_order = np.argsort(E)
                E = E[sort_order]
                v = v[:, sort_order]
                old_psi0_1q = psi0_1q
                psi0_1q = v[:, 0]
                psi0_complete = U @ (np.append(psi0_1q, np.zeros(SG.M // 2)))

                h_array.append(h)
                fidelities.append(
                    np.abs(np.vdot(psi0_1q, old_psi0_1q))
                    if old_psi0_1q is not None
                    else 1
                )
                e_gaps.append(E[1] - E[0])
                total_gs_probs.append(
                    np.sum(psi0_complete[instance.ground_states] ** 2)
                )
            except:
                diag_failure = True

            if diag_failure or (
                i > 1
                and total_gs_probs[i] > 0.99
                and fidelities[i] > 0.99
                and fidelities[i - 1] > 0.99
            ):
                break

            h /= 2 if i % 2 == 0 else 5
            i += 1

        if i > 1:
            gs_probs = 2 * psi0_complete[instance.reduced_gs] ** 2
            instance.post_anneal_gs_probs = gs_probs.tolist()
            instance.post_anneal_supp_ratio = round(
                1 - (np.min(gs_probs) / np.max(gs_probs)), 6
            )

            instance.diag_run_h_array = h_array
            instance.diag_run_fidelities = fidelities
            instance.diag_run_e_gaps = e_gaps

        else:
            instance.post_anneal_gs_probs = None
            instance.post_anneal_supp_ratio = None

            instance.diag_run_h_array = None
            instance.diag_run_fidelities = None
            instance.diag_run_e_gaps = None

        instance.diag_run_failure = diag_failure

    session.commit()

    session.close()
