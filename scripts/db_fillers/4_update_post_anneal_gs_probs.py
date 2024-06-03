import numpy as np

from database.models import InstancesN8, InstancesN12
from tfim_sk_infd.services import qutip_service
from tfim_sk_infd.models.Jij import Jij
from tfim_sk_infd.models.SKSpinGlass import SKSpinGlass
import data_service
from tqdm import tqdm
from scipy.sparse import linalg as spla

N = 12


Instance = data_service.get_instance_class(N)


with data_service.get_session() as session:

    instances: list[InstancesN8 | InstancesN12] = (
        session.query(Instance).where(Instance.degeneracy > 2).all()
    )

    for instance in tqdm(instances):

        try:

            Jij_obj = Jij(np.array(instance.Jij_matrix))

            SG = SKSpinGlass(Jij_obj)

            # initial diag
            h = 0.1
            H = SG.hamiltonian_at_h(h)
            E, v = spla.eigsh(H, k=instance.degeneracy + 1, which="SA")

            sort_order = np.argsort(E)
            E = E[sort_order]
            v = v[:, sort_order]
            psi0 = v[:, 0]

            min_e_gap = E[1] - E[0]
            if min_e_gap < 1e-15:
                raise Exception(
                    f"Diagonalization fail for seed {instance.seed} with min_e_gap {min_e_gap} at h = {h}"
                )

            fidelity = 0
            while fidelity < 0.99:
                h /= 2
                H = SG.hamiltonian_at_h(h)
                E, v = spla.eigsh(H, k=2, which="SA", v0=psi0)

                sort_order = np.argsort(E)
                E = E[sort_order]
                v = v[:, sort_order]

                old_psi0 = psi0
                psi0 = v[:, 0]

                min_e_gap = E[1] - E[0]
                if min_e_gap < 1e-15:
                    raise Exception(
                        f"Diagonalization fail for seed {instance.seed} with min_e_gap {min_e_gap} at h = {h}"
                    )

                fidelity = np.abs(np.inner(psi0, old_psi0))

            gs_probs = 2 * psi0[instance.reduced_gs] ** 2
            instance.post_anneal_gs_probs = gs_probs.tolist()
            instance.post_anneal_supp_ratio = round(
                1 - (np.min(gs_probs) / np.max(gs_probs)), 6
            )

        except Exception as e:
            print(
                f"Diagonalization fail for seed {instance.seed}, min_e_gap {min_e_gap}, h {h}, fidelity {fidelity}\norgiginal error:\n{e}"
            )

    session.commit()

    session.close()
