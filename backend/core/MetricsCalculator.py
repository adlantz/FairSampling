import numpy as np
from core.helper import base_N_hamming_distance
from typing import Optional
from numpy import linalg


class MetricsCalculator:
    def __init__(self, N: int, ground_states: list, gs_probs: Optional[list] = None):
        self.N = N
        self.ground_states = ground_states
        self.gs_probs = gs_probs
        self.od_bins = od_bins = np.array([((2 * i) / N) - 1 for i in range(N + 1)])

    def _overlap_distribution_fair(self, gs_list: list[int], N: int) -> np.ndarray:
        gs_size = len(gs_list)
        overlap_dist = np.zeros(N + 1)
        overlap_dist[-1] = 1 / gs_size  # (gs_size / gs_size^2)
        for i in range(gs_size):
            for j in range(i + 1, gs_size):
                h_d = base_N_hamming_distance(gs_list[i], gs_list[j])
                overlap_dist[-h_d - 1] += 2 / (gs_size**2)
        return overlap_dist

    def _overlap_distribution_weighted(
        self, gs_list: list[int], gs_probs: list[float], N: int
    ) -> np.ndarray:
        gs_size = len(gs_list)
        overlap_dist = np.zeros(N + 1)
        for i in range(gs_size):
            for j in range(i, gs_size):
                h_d = base_N_hamming_distance(gs_list[i], gs_list[j])
                overlap_dist[-h_d - 1] += (
                    (1 if i == j else 2) * gs_probs[i] * gs_probs[j]
                )
        return overlap_dist

    def calculate_metrics(self) -> dict:

        metrics_dict = {}

        fs_od = self._overlap_distribution_fair(self.ground_states, self.N)
        fs_od_mean = np.sum(self.od_bins * fs_od)
        metrics_dict["fs_od"] = fs_od.tolist()
        metrics_dict["fs_od_mean"] = fs_od_mean
        metrics_dict["fs_od_var"] = np.sum(fs_od * (self.od_bins - fs_od_mean) ** 2)

        # Compute H (symmetric Hamming distance matrix)
        deg = len(self.ground_states)

        H = np.zeros((deg, deg))
        for i in range(deg):
            for j in range(i + 1, deg):
                H[i][j] = H[j][i] = base_N_hamming_distance(
                    self.ground_states[i], self.ground_states[j]
                )

        metrics_dict["fs_qfi"] = max(
            (4 / deg)
            * ((linalg.norm(H, axis=1)) ** 2 - (1 / deg) * (np.sum(H, axis=1)) ** 2)
        ) / (self.N**2)

        if self.gs_probs is not None:
            P = np.zeros((deg, deg))
            for i in range(deg):
                for j in range(i + 1, deg):
                    P[i][j] = self.gs_probs[j]
                    P[j][i] = self.gs_probs[i]
            pa_od = self._overlap_distribution_weighted(
                self.ground_states, self.gs_probs, self.N
            )
            pa_od_mean = np.sum(self.od_bins * pa_od)
            metrics_dict["pa_od"] = pa_od.tolist()
            metrics_dict["pa_od_mean"] = pa_od_mean
            metrics_dict["pa_od_var"] = np.sum(pa_od * (self.od_bins - pa_od_mean) ** 2)

            metrics_dict["pa_qfi"] = max(
                4 * (np.sum(H * H * P, axis=1) - np.sum(H * P, axis=1) ** 2)
            ) / (self.N**2)

        return metrics_dict
