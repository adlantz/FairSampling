# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains research code for exploring quantum annealing on Ising model spin glasses. The research examines entanglement structure and "macroscopic quantumness" as it relates to computational hardness and the efficacy of quantum adiabatic computation.

## Architecture

The codebase has evolved and contains two parallel implementations:

### Legacy Implementation
- **`tfim_sk_infd/`**: Original package-style implementation with models and services
  - `models/`: Contains `IsingBasis`, `Jij`, `SKSpinGlass`, and `branchboundV11.py` (branch-and-bound solver)
  - `services/`: Contains `ground_state_service`, `jij_service`, `qutip_service`, `entropy_service`, `large_n_service`
- **`database/`**: Legacy SQLAlchemy database with size-specific tables (`InstancesN8`, `InstancesN12`, `InstancesN16`, `InstancesN18`, `InstancesN20`, `LargeN`)
  - Uses Alembic for migrations (`database/alembic/`)
  - Database file: `database/fair_sampling.db`
- **`scripts/db_fillers/`**: Scripts (0-9) to populate the legacy database with computed metrics
  - Run via Makefile targets (`db_fill_0` through `db_fill_8`)

### Modern Implementation (backend/)
- **`backend/`**: Newer FastAPI-based implementation
  - `api.py`: FastAPI server with job submission and query endpoints (with CORS enabled for localhost:3000)
  - `core/`: Refactored core computation modules
    - `Jij.py`: Coupling matrix generation
    - `BranchBoundSolver.py`: Ground state solver
    - `QuantumSpinGlass.py`: Quantum annealing simulation
    - `MetricsCalculator.py`: Computes overlap distribution, QFI, etc.
    - `JobRunner.py`: Orchestrates computation pipeline
    - `IsingBasis.py`: Ising basis utilities
    - `helper.py`: Contains `maximal_half_clique` for reduced ground state calculation
  - `database/`: SQLModel-based database with unified table structure
    - Tables: `Instance`, `InstanceGroundStates`, `InstancePostAnnealingInfo`, `InstanceMetrics`, `Job`
    - Database file: `backend/database/local.db`

### Frontend (frontend/)
- **`frontend/`**: Next.js 14+ React application with TypeScript
  - Built with App Router (not Pages Router)
  - Uses Tailwind CSS for styling
  - React Query (@tanstack/react-query) for API state management
  - Three main sections:
    - Job submission form for creating computation jobs
    - Job status monitoring with auto-refresh
    - Instance data viewer for querying results
  - `lib/api.ts`: API client functions using axios
  - `lib/types.ts`: TypeScript types matching backend models

## Key Concepts

- **Instances**: Characterized by system size `N` and random `seed`, each instance has a unique Jij coupling matrix
- **Ground States**: Computed via branch-and-bound algorithm; instances may have degenerate ground states
- **Reduced Ground States**: For highly degenerate cases, a maximal half-clique subset is used
- **Post-Annealing Info**: Results from quantum annealing simulation including ground state probabilities, suppression ratio, fidelity, and energy gaps
- **Metrics**: Overlap distribution (OD), overlap distribution variance, quantum Fisher information (QFI)
- **Fair Sampling**: Assumes equal probability across ground states; compared against post-annealing results

## Development Workflow

### Running Database Population Scripts (Legacy)

Individual scripts via Makefile:
```bash
make db_fill_0  # Add instances
make db_fill_1  # Update degeneracy
make db_fill_2  # Update reduced ground state Hamming distance
make db_fill_3  # Update overlap distribution
make db_fill_4  # Update post-anneal ground state probabilities
make db_fill_5  # Update post-anneal overlap
make db_fill_6  # Update disconnectivity
make db_fill_7  # Update QFI
make db_fill_8  # Update distance
```

Complete pipeline via shell script:
```bash
./add_data.sh <N> <seed_start> <seed_end> <batch_size>
```

### Running Backend API

Start the FastAPI server (from repository root):
```bash
python -m uvicorn backend.api:app --reload
```

The API will be available at `http://localhost:8000` with the following endpoints:
- `GET /`: Welcome message
- `POST /submit_job`: Submit a computation job (returns job ID)
- `GET /job_status/{job_id}`: Check job status
- `GET /instances/{N}/{seed}`: Get instance data
- `GET /ground_states/{N}/{seed}`: Get ground states
- `GET /post_annealing_info/{N}/{seed}`: Get post-annealing results

### Running Frontend

Start the development server (from `frontend/` directory):
```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`.

Build for production:
```bash
cd frontend
npm run build
npm start
```

### Running Backend and Frontend Together

In one terminal:
```bash
python -m uvicorn backend.api:app --reload
```

In another terminal:
```bash
cd frontend && npm run dev
```

Then open `http://localhost:3000` in your browser.

### Database Management

Legacy database (SQLAlchemy + Alembic):
```bash
cd database
alembic revision --autogenerate -m "description"
alembic upgrade head
```

Backend database (SQLModel):
- Located at `backend/database/local.db`
- Models defined in `backend/database/models.py`
- Session management in `backend/database/database.py`

### Exploration Notebooks

Jupyter notebooks for research exploration are in `exploration_notebooks/`. These notebooks are used to develop and test ideas before converting them into production scripts.

### Data Service

`data_service.py` provides utilities to:
- Get database sessions for the legacy database
- Save/load JSON files locally in `data/` directories
- Map system size `N` to appropriate instance table class

## Dependencies

### Backend Dependencies

Install Python dependencies via:
```bash
pip install -r requirements.txt
```

Key dependencies: numpy, scipy, qutip (quantum toolbox), sqlalchemy, alembic, fastapi, sqlmodel, mosek (optimization), networkx, pandas, tqdm, matplotlib

### Frontend Dependencies

Install Node.js dependencies:
```bash
cd frontend
npm install
```

Key dependencies: next, react, react-dom, axios, @tanstack/react-query, tailwindcss, typescript

## Virtual Environment

The project uses a Python virtual environment at `.venv/`. Activate before backend development:
```bash
source .venv/bin/activate
```
