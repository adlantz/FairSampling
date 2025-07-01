from uuid import UUID
from sqlmodel import Session, select
from database.database import engine
from database.models import (
    Job,
    Instance,
    InstanceGroundStates,
    InstancePostAnnealingInfo,
    InstanceMetrics,
)
from core.Jij import Jij
from core.BranchBoundSolver import BB
from core.QuantumSpinGlass import QuantumSpinGlass
from core.MetricsCalculator import MetricsCalculator
from core.helper import maximal_half_clique
import numpy as np
from tqdm import tqdm
from typing import Optional


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
                instance_post_annealing_info = (
                    self._run_annealing(instance, instance_ground_states)
                    if self.params.get("annealing")
                    else None
                )

                if self.params.get("metrics"):
                    self._calculate_metrics(
                        instance, instance_ground_states, instance_post_annealing_info
                    )

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

    def _calculate_ground_states(self, instance: Instance) -> InstanceGroundStates:
        Q2 = Jij(np.array(instance.jij_matrix)).full_Jij_matrix()
        P2 = Q2.sum(axis=1)
        R2 = Q2.sum()
        ground_states = BB(-2 * Q2, 2 * P2, -0.5 * R2).get_ground_states()
        degeneracy = len(ground_states)
        reduced_gs = (
            maximal_half_clique(ground_states, self.N) if degeneracy > 2 else None
        )
        record = InstanceGroundStates(
            N=instance.N,
            seed=instance.seed,
            ground_states=ground_states,
            reduced_gs=reduced_gs,
            degeneracy=degeneracy,
        )
        self.session.merge(record)
        self.session.commit()
        return record

    def _run_annealing(
        self, instance: Instance, instance_ground_states: InstanceGroundStates
    ) -> InstancePostAnnealingInfo:
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
        return record

    def _calculate_metrics(
        self,
        instance: Instance,
        instance_ground_states: InstanceGroundStates,
        instance_post_annealing_info: Optional[InstancePostAnnealingInfo] = None,
    ) -> None:
        metrics_dict = MetricsCalculator(
            self.N,
            instance_ground_states.ground_states,
            instance_post_annealing_info and instance_post_annealing_info.gs_amplitudes,
        ).calculate_metrics()

        record = InstanceMetrics(
            N=self.N,
            seed=instance.seed,
            fs_od=metrics_dict.get("fs_od"),
            fs_od_mean=metrics_dict.get("fs_od_mean"),
            fs_od_var=metrics_dict.get("fs_od_var"),
            fs_qfi=metrics_dict.get("fs_qfi"),
            pa_od=metrics_dict.get("pa_od"),
            pa_od_mean=metrics_dict.get("pa_od_mean"),
            pa_od_var=metrics_dict.get("pa_od_var"),
            pa_qfi=metrics_dict.get("pa_qfi"),
        )

        self.session.merge(record)
        self.session.commit()
