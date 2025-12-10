import axios from 'axios';
import type {
  Instance,
  InstanceGroundStates,
  InstancePostAnnealingInfo,
  JobRequest,
  JobStatusResponse,
} from './types';

// Configure axios with base URL
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Functions

export const submitJob = async (jobRequest: JobRequest): Promise<string> => {
  const response = await api.post<{ job_id: string }>('/submit_job', jobRequest);
  return response.data.job_id;
};

export const getJobStatus = async (jobId: string): Promise<JobStatusResponse> => {
  const response = await api.get<JobStatusResponse>(`/job_status/${jobId}`);
  return response.data;
};

export const getInstance = async (N: number, seed: number): Promise<Instance> => {
  const response = await api.get<Instance>(`/instances/${N}/${seed}`);
  return response.data;
};

export const getGroundStates = async (N: number, seed: number): Promise<InstanceGroundStates> => {
  const response = await api.get<InstanceGroundStates>(`/ground_states/${N}/${seed}`);
  return response.data;
};

export const getPostAnnealingInfo = async (N: number, seed: number): Promise<InstancePostAnnealingInfo> => {
  const response = await api.get<InstancePostAnnealingInfo>(`/post_annealing_info/${N}/${seed}`);
  return response.data;
};

export default api;
