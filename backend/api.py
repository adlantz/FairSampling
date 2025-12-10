from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from database.database import engine
from database.models import (
    Instance,
    InstanceGroundStates,
    InstancePostAnnealingInfo,
    Job,
)
from core.JobRunner import JobRunner
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, UTC


app = FastAPI()

# Configure CORS - more permissive for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for debugging
    allow_credentials=False,  # Set to False when using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get DB session
def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
def read_root():
    return {"message": "Welcome to the FairSampling API!"}


@app.get("/instances/{N}/{seed}", response_model=Instance)
def get_instance(N: int, seed: int):
    with Session(engine) as session:
        instance = session.get(Instance, (N, seed))
        if not instance:
            raise HTTPException(status_code=404, detail="Instance not found")
        return instance


@app.get("/ground_states/{N}/{seed}", response_model=InstanceGroundStates)
def get_ground_states(N: int, seed: int):
    with Session(engine) as session:
        gs = session.get(InstanceGroundStates, (N, seed))
        if not gs:
            raise HTTPException(status_code=404, detail="Ground states not found")
        return gs


@app.get("/post_annealing_info/{N}/{seed}", response_model=InstancePostAnnealingInfo)
def get_post_annealing_info(N: int, seed: int):
    with Session(engine) as session:
        info = session.get(InstancePostAnnealingInfo, (N, seed))
        if not info:
            raise HTTPException(status_code=404, detail="Post annealing info not found")
        return info


from pydantic import BaseModel


class JobParams(BaseModel):
    N: int
    seed_start: int
    seed_end: int
    ground_states: bool
    annealing: bool
    metrics: bool
    recalculate: bool


class JobRequest(BaseModel):
    params: JobParams


def run_job(job_id: UUID, params: dict):
    runner = JobRunner(job_id, params)
    runner.run()


@app.post("/submit_job")
async def submit_job(request: Request, background_tasks: BackgroundTasks):
    # Log the raw request body for debugging
    body = await request.json()
    print("Received request body:", body)

    try:
        job_request = JobRequest(**body)
    except Exception as e:
        print("Validation error:", str(e))
        raise HTTPException(status_code=400, detail=str(e))

    job = Job(
        params=job_request.params.model_dump(),  # Convert Pydantic model to dict
        status="pending",
        submitted_at=datetime.now(UTC),
    )

    with Session(engine) as session:
        session.add(job)
        session.commit()
        session.refresh(job)

    background_tasks.add_task(run_job, job.id, job_request.params.model_dump())

    return {"job_id": str(job.id)}


@app.get("/job_status/{job_id}")
def get_job_status(job_id: UUID):
    with Session(engine) as session:
        job = session.get(Job, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return {"id": job.id, "status": job.status}
