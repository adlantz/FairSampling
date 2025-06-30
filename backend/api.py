from fastapi import FastAPI, HTTPException, BackgroundTasks
from sqlmodel import Session, select
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


# Dependency to get DB session
def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
def read_root():
    return {"message": "Welcome to the FairSampling API!"}


@app.get("/instances/{seed}", response_model=Instance)
def get_instance(seed: int):
    with Session(engine) as session:
        instance = session.get(Instance, seed)
        if not instance:
            raise HTTPException(status_code=404, detail="Instance not found")
        return instance


@app.get("/ground_states/{seed}", response_model=InstanceGroundStates)
def get_ground_states(seed: int):
    with Session(engine) as session:
        gs = session.get(InstanceGroundStates, seed)
        if not gs:
            raise HTTPException(status_code=404, detail="Ground states not found")
        return gs


@app.get("/post_annealing_info/{seed}", response_model=InstancePostAnnealingInfo)
def get_post_annealing_info(seed: int):
    with Session(engine) as session:
        info = session.get(InstancePostAnnealingInfo, seed)
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


@app.post("/submit_job", response_model=UUID)
def submit_job(job_request: JobRequest, background_tasks: BackgroundTasks):
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

    return job.id


@app.get("/job_status/{job_id}")
def get_job_status(job_id: UUID):
    with Session(engine) as session:
        job = session.get(Job, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return {"id": job.id, "status": job.status}
