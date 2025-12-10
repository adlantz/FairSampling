// API Model Types

export interface Instance {
  N: number;
  seed: number;
  jij_matrix?: Record<string, unknown>;
  bonds?: string;
}

export interface InstanceGroundStates {
  N: number;
  seed: number;
  ground_states?: number[];
  reduced_gs?: number[];
  degeneracy?: number;
}

export interface InstancePostAnnealingInfo {
  N: number;
  seed: number;
  gs_amplitudes?: number[];
  suppression_ratio?: number;
  diag_run_h_array?: number[];
  diag_run_fidelities?: number[];
  diag_run_e_gaps?: number[];
  diag_run_failure?: boolean;
}

export interface InstanceMetrics {
  N: number;
  seed: number;
  fs_od?: Record<string, unknown>;
  fs_od_mean?: number;
  fs_od_var?: number;
  fs_qfi?: number;
  pa_od?: Record<string, unknown>;
  pa_od_mean?: number;
  pa_od_var?: number;
  pa_qfi?: number;
}

export interface JobParams {
  N: number;
  seed_start: number;
  seed_end: number;
  ground_states: boolean;
  annealing: boolean;
  metrics: boolean;
  recalculate: boolean;
}

export interface JobRequest {
  params: JobParams;
}

export interface Job {
  id: string;
  params?: JobParams;
  status?: string;
  submitted_at?: string;
}

export interface JobStatusResponse {
  id: string;
  status: string;
}
