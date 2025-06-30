from uuid import UUID
from sqlmodel import Session, select
from database.database import engine
from database.models import (
    Job,
    Instance,
    InstanceGroundStates,
    InstancePostAnnealingInfo,
)
from core.Jij import Jij
from core.BranchBoundSolver import BB
from core.QuantumSpinGlass import QuantumSpinGlass
import numpy as np
from tqdm import tqdm


class JobRunner:
    def __init__(self, job_id: UUID, params: dict):
        self.job_id = job_id
        self.params = params
        self.N = params["N"]
        self.seed_start = params["seed_start"]
        self.seed_end = params["seed_end"]
        self.recalculate = params.get("recalculate", False)
        self.session = Session(engine)

    def run(self):
        try:
            print("starting job")
            print(self.params)
            self._update_status("running")

            for seed in tqdm(range(self.seed_start, self.seed_end + 1)):

                instance = self._generate_instance(self.N, seed)
                instance_ground_states = self._calculate_ground_states(instance)

                if self.params.get("annealing"):
                    self._run_annealing(instance, instance_ground_states)

                if self.params.get("metrics"):
                    self._calculate_metrics(seed)

            self._update_status("successful")
        except Exception as e:
            self._update_status("failed")
            raise e
        finally:
            self.session.close()

    def _update_status(self, status: str):
        job = self.session.get(Job, self.job_id)
        if job:
            job.status = status
            self.session.add(job)
            self.session.commit()

    def _generate_instance(self, N: int, seed: int):
        record = Instance(
            N=N, seed=seed, jij_matrix=Jij.generate(N, seed).to_json(), bonds="full"
        )
        self.session.merge(record)
        self.session.commit()
        return record

    def _calculate_ground_states(self, instance):
        Q2 = Jij(np.array(instance.jij_matrix)).full_Jij_matrix()
        P2 = Q2.sum(axis=1)
        R2 = Q2.sum()
        ground_states = BB(-2 * Q2, 2 * P2, -0.5 * R2).get_ground_states()
        record = InstanceGroundStates(
            N=instance.N, seed=instance.seed, ground_states=ground_states
        )
        self.session.merge(record)
        self.session.commit()
        return record

    def _run_annealing(self, instance, instance_ground_states):
        QSG = QuantumSpinGlass(
            Jij(np.array(instance.jij_matrix)), instance_ground_states.ground_states
        )
        (
            gs_probs,
            suppression_ratio,
            h_array,
            fidelities,
            e_gaps,
            diag_failure,
        ) = QSG.get_post_anneal_info()
        record = InstancePostAnnealingInfo(
            N=instance.N,
            seed=instance.seed,
            gs_amplitudes=gs_probs,
            suppression_ratio=suppression_ratio,
            diag_run_h_array=h_array,
            diag_run_fidelities=fidelities,
            diag_run_e_gaps=e_gaps,
            diag_run_failure=diag_failure,
        )
        self.session.merge(record)
        self.session.commit()

        # add your computation here

    def _calculate_metrics(self, seed):
        pass
        # add your computation here
