# FairSampling Frontend

Next.js TypeScript application for the FairSampling quantum annealing research project.

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Configure the API URL (optional):
```bash
cp .env.example .env.local
# Edit .env.local if your backend is not running on http://localhost:8000
```

3. Start the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Features

### Job Submission
- Configure computation parameters (N, seed range)
- Select which computations to run (ground states, annealing, metrics)
- Submit jobs and receive job IDs

### Job Monitoring
- Add job IDs to monitor their status
- Auto-refresh for pending/running jobs every 3 seconds
- View job status (pending, running, successful, failed)

### Instance Data Viewer
- Query instance data by N and seed
- View three data types:
  - Instance: Jij matrix and coupling configuration
  - Ground States: Ground state list, degeneracy, reduced ground states
  - Post-Annealing: Amplitudes, fidelities, energy gaps, suppression ratio

## Tech Stack

- **Next.js 14+**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **React Query**: Server state management with automatic caching and refetching
- **Axios**: HTTP client for API requests

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx       # Root layout with providers
│   ├── page.tsx         # Main page with all sections
│   ├── providers.tsx    # React Query provider setup
│   └── globals.css      # Global styles and Tailwind imports
├── lib/
│   ├── api.ts           # API client functions
│   └── types.ts         # TypeScript type definitions
└── package.json         # Dependencies and scripts
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Backend Connection

The frontend expects the FastAPI backend to be running at `http://localhost:8000`. Make sure to:

1. Start the backend server first:
```bash
# From repository root
python -m uvicorn backend.api:app --reload
```

2. Then start the frontend:
```bash
cd frontend
npm run dev
```
