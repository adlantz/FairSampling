import numpy as np

from database.models import InstancesN8
from tfim_sk_infd.services import ground_state_service, qutip_service
from tfim_sk_infd.models.Jij import Jij
import data_service

N = 8
h = 1e-1


with data_service.get_session() as session:

    instances = (
        session.query(InstancesN8)
        .where(
            (InstancesN8.degeneracy > 2) & (InstancesN8.post_anneal_gs_probs.is_(None))
        )
        .all()
    )

    Ht = qutip_service.transverse_field_hamiltonian(N)
    for instance in instances:

        Jij_obj = Jij(np.array(instance.Jij_matrix))

        Hp = qutip_service.spin_glass_hamiltonian(Jij_obj, N)

        h_t = -Hp - h * Ht

        eigenvalues, eigenstates = h_t.eigenstates(eigvals=1)

        gs_probs = [
            round(2 * float(pa.real**2 + pa.imag**2), 5)
            for pa in eigenstates[0].full().flatten()[instance.reduced_gs]
        ]

        if abs(sum(gs_probs) - 1) > 1e-1:
            print(
                f"seed {instance.seed} diagonalization fail. gs prob array sum {sum(gs_probs)}\n{gs_probs}"
            )
            continue

        instance.post_anneal_gs_probs = gs_probs
        instance.post_anneal_supp_ratio = 1 - (min(gs_probs) / max(gs_probs))

    session.commit()

    session.close()
