'use client';

import { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { submitJob, getJobStatus, getInstance, getGroundStates, getPostAnnealingInfo } from '@/lib/api';
import type { JobParams } from '@/lib/types';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <header className="bg-white dark:bg-gray-800 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            FairSampling Research Interface
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Quantum Annealing on Ising Model Spin Glasses
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 space-y-8">
        <JobSubmissionSection />
        <JobMonitoringSection />
        <InstanceViewerSection />
      </main>
    </div>
  );
}

function JobSubmissionSection() {
  const [params, setParams] = useState<JobParams>({
    N: 12,
    seed_start: 1,
    seed_end: 10,
    ground_states: true,
    annealing: true,
    metrics: true,
    recalculate: false,
  });

  const mutation = useMutation({
    mutationFn: (jobParams: JobParams) => submitJob({ params: jobParams }),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate(params);
  };

  return (
    <section className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 className="text-2xl font-semibold mb-4 text-gray-900 dark:text-white">
        Submit Computation Job
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              System Size (N)
            </label>
            <input
              type="number"
              value={params.N}
              onChange={(e) => setParams({ ...params, N: parseInt(e.target.value) || 0 })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              min="1"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Seed Start
            </label>
            <input
              type="number"
              value={params.seed_start}
              onChange={(e) => setParams({ ...params, seed_start: parseInt(e.target.value) || 0 })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              min="1"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Seed End
            </label>
            <input
              type="number"
              value={params.seed_end}
              onChange={(e) => setParams({ ...params, seed_end: parseInt(e.target.value) || 0 })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              min="1"
              required
            />
          </div>
        </div>

        <div className="space-y-2">
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={params.ground_states}
              onChange={(e) => setParams({ ...params, ground_states: e.target.checked })}
              className="rounded border-gray-300 dark:border-gray-600"
            />
            <span className="text-sm text-gray-700 dark:text-gray-300">Calculate Ground States</span>
          </label>

          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={params.annealing}
              onChange={(e) => setParams({ ...params, annealing: e.target.checked })}
              className="rounded border-gray-300 dark:border-gray-600"
            />
            <span className="text-sm text-gray-700 dark:text-gray-300">Run Annealing Simulation</span>
          </label>

          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={params.metrics}
              onChange={(e) => setParams({ ...params, metrics: e.target.checked })}
              className="rounded border-gray-300 dark:border-gray-600"
            />
            <span className="text-sm text-gray-700 dark:text-gray-300">Calculate Metrics</span>
          </label>

          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={params.recalculate}
              onChange={(e) => setParams({ ...params, recalculate: e.target.checked })}
              className="rounded border-gray-300 dark:border-gray-600"
            />
            <span className="text-sm text-gray-700 dark:text-gray-300">Recalculate Existing</span>
          </label>
        </div>

        <button
          type="submit"
          disabled={mutation.isPending}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-1.5 px-6 rounded-md transition-colors"
        >
          {mutation.isPending ? 'Submitting...' : 'Submit Job'}
        </button>

        {mutation.isSuccess && (
          <div className="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-md">
            <p className="text-green-800 dark:text-green-200">
              Job submitted successfully! Job ID: <code className="font-mono text-sm">{mutation.data}</code>
            </p>
          </div>
        )}

        {mutation.isError && (
          <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md">
            <p className="text-red-800 dark:text-red-200">
              Error: {mutation.error instanceof Error ? mutation.error.message : 'Failed to submit job'}
            </p>
          </div>
        )}
      </form>
    </section>
  );
}

function JobMonitoringSection() {
  const [jobIds, setJobIds] = useState<string[]>([]);
  const [newJobId, setNewJobId] = useState('');

  const addJobId = () => {
    if (newJobId && !jobIds.includes(newJobId)) {
      setJobIds([...jobIds, newJobId]);
      setNewJobId('');
    }
  };

  const removeJobId = (id: string) => {
    setJobIds(jobIds.filter(jobId => jobId !== id));
  };

  return (
    <section className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 className="text-2xl font-semibold mb-4 text-gray-900 dark:text-white">
        Job Status Monitoring
      </h2>

      <div className="space-y-2 mb-4">
        <button
          onClick={addJobId}
          className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-1.5 px-4 rounded-md transition-colors"
        >
          Add Job ID
        </button>
        <input
          type="text"
          value={newJobId}
          onChange={(e) => setNewJobId(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && addJobId()}
          placeholder="Enter Job ID to monitor"
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
        />
      </div>

      <div className="space-y-3">
        {jobIds.length === 0 ? (
          <p className="text-gray-500 dark:text-gray-400 text-center py-8">
            No jobs being monitored. Add a job ID above to start monitoring.
          </p>
        ) : (
          jobIds.map(jobId => (
            <JobStatusCard key={jobId} jobId={jobId} onRemove={() => removeJobId(jobId)} />
          ))
        )}
      </div>
    </section>
  );
}

function JobStatusCard({ jobId, onRemove }: { jobId: string; onRemove: () => void }) {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['jobStatus', jobId],
    queryFn: () => getJobStatus(jobId),
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      return status === 'pending' || status === 'running' ? 3000 : false;
    },
  });

  const getStatusColor = (status?: string) => {
    switch (status) {
      case 'successful':
        return 'bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-200';
      case 'failed':
        return 'bg-red-100 dark:bg-red-900/20 text-red-800 dark:text-red-200';
      case 'running':
        return 'bg-blue-100 dark:bg-blue-900/20 text-blue-800 dark:text-blue-200';
      case 'pending':
        return 'bg-yellow-100 dark:bg-yellow-900/20 text-yellow-800 dark:text-yellow-200';
      default:
        return 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200';
    }
  };

  return (
    <div className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-md">
      <div className="flex-1">
        <p className="font-mono text-sm text-gray-600 dark:text-gray-400 mb-1">
          {jobId}
        </p>
        {isLoading && <p className="text-sm text-gray-500 dark:text-gray-400">Loading...</p>}
        {error && <p className="text-sm text-red-600 dark:text-red-400">Error loading status</p>}
        {data && (
          <span className={`inline-block px-2 py-1 text-xs font-medium rounded ${getStatusColor(data.status)}`}>
            {data.status}
          </span>
        )}
      </div>
      <div className="flex gap-2">
        <button
          onClick={() => refetch()}
          className="text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 text-sm"
        >
          Refresh
        </button>
        <button
          onClick={onRemove}
          className="text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300 text-sm"
        >
          Remove
        </button>
      </div>
    </div>
  );
}

function InstanceViewerSection() {
  const [N, setN] = useState(12);
  const [seed, setSeed] = useState(1);
  const [activeTab, setActiveTab] = useState<'instance' | 'ground_states' | 'post_annealing' | null>(null);

  const instanceQuery = useQuery({
    queryKey: ['instance', N, seed],
    queryFn: () => getInstance(N, seed),
    enabled: activeTab === 'instance',
  });

  const groundStatesQuery = useQuery({
    queryKey: ['groundStates', N, seed],
    queryFn: () => getGroundStates(N, seed),
    enabled: activeTab === 'ground_states',
  });

  const postAnnealingQuery = useQuery({
    queryKey: ['postAnnealing', N, seed],
    queryFn: () => getPostAnnealingInfo(N, seed),
    enabled: activeTab === 'post_annealing',
  });

  return (
    <section className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 className="text-2xl font-semibold mb-4 text-gray-900 dark:text-white">
        Instance Data Viewer
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            System Size (N)
          </label>
          <input
            type="number"
            value={N}
            onChange={(e) => setN(parseInt(e.target.value) || 0)}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            min="1"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Seed
          </label>
          <input
            type="number"
            value={seed}
            onChange={(e) => setSeed(parseInt(e.target.value) || 0)}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            min="1"
          />
        </div>
      </div>

      <div className="flex gap-2 mb-4">
        <button
          onClick={() => setActiveTab('instance')}
          className={`px-4 py-2 rounded-md font-medium transition-colors ${
            activeTab === 'instance'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
          }`}
        >
          Instance
        </button>
        <button
          onClick={() => setActiveTab('ground_states')}
          className={`px-4 py-2 rounded-md font-medium transition-colors ${
            activeTab === 'ground_states'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
          }`}
        >
          Ground States
        </button>
        <button
          onClick={() => setActiveTab('post_annealing')}
          className={`px-4 py-2 rounded-md font-medium transition-colors ${
            activeTab === 'post_annealing'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
          }`}
        >
          Post-Annealing
        </button>
      </div>

      <div className="border border-gray-200 dark:border-gray-700 rounded-md p-4 min-h-[200px]">
        {!activeTab && (
          <p className="text-gray-500 dark:text-gray-400 text-center py-8">
            Select a data type above to view instance data
          </p>
        )}

        {activeTab === 'instance' && (
          <DataDisplay
            data={instanceQuery.data}
            isLoading={instanceQuery.isLoading}
            error={instanceQuery.error}
          />
        )}

        {activeTab === 'ground_states' && (
          <DataDisplay
            data={groundStatesQuery.data}
            isLoading={groundStatesQuery.isLoading}
            error={groundStatesQuery.error}
          />
        )}

        {activeTab === 'post_annealing' && (
          <DataDisplay
            data={postAnnealingQuery.data}
            isLoading={postAnnealingQuery.isLoading}
            error={postAnnealingQuery.error}
          />
        )}
      </div>
    </section>
  );
}

function DataDisplay({ data, isLoading, error }: { data: unknown; isLoading: boolean; error: Error | null }) {
  if (isLoading) {
    return <p className="text-gray-500 dark:text-gray-400">Loading...</p>;
  }

  if (error) {
    return (
      <div className="text-red-600 dark:text-red-400">
        <p className="font-medium">Error loading data:</p>
        <p className="text-sm mt-1">{error.message}</p>
      </div>
    );
  }

  if (!data) {
    return <p className="text-gray-500 dark:text-gray-400">No data available</p>;
  }

  return (
    <pre className="text-xs overflow-auto bg-gray-50 dark:bg-gray-900 p-4 rounded">
      {JSON.stringify(data, null, 2)}
    </pre>
  );
}
