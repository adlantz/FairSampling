from sqlmodel import SQLModel, Field, DateTime
from sqlalchemy import Column, JSON
from typing import Optional, Dict, List
from uuid import UUID, uuid4
from datetime import datetime, UTC


class Instance(SQLModel, table=True):
    N: int = Field(primary_key=True)
    seed: int = Field(primary_key=True)
    jij_matrix: Optional[Dict] = Field(sa_column=Column(JSON))
    bonds: Optional[str] = None


class InstanceGroundStates(SQLModel, table=True):
    N: int = Field(primary_key=True)
    seed: int = Field(primary_key=True)
    ground_states: Optional[List] = Field(sa_column=Column(JSON))


class InstancePostAnnealingInfo(SQLModel, table=True):
    N: int = Field(primary_key=True)
    seed: int = Field(primary_key=True)
    gs_amplitudes: Optional[List[float]] = Field(sa_column=Column(JSON))
    suppression_ratio: Optional[float] = None
    diag_run_h_array: Optional[List[float]] = Field(sa_column=Column(JSON))
    diag_run_fidelities: Optional[List[float]] = Field(sa_column=Column(JSON))
    diag_run_e_gaps: Optional[List[float]] = Field(sa_column=Column(JSON))
    diag_run_failure: Optional[bool] = None


class Job(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    params: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    status: Optional[str] = None
    submitted_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(DateTime(timezone=True)),
    )
