from sqlalchemy import Column, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Define Python objects here that correspond to tables in the db
class InstancesN8(Base):
    __tablename__ = "instances_N8"
    seed = Column(Integer, primary_key=True)
    Jij_matrix = Column(JSON, nullable=False)
    ground_states = Column(JSON, nullable=False)
    degeneracy = Column(Integer, nullable=True)
    reduced_gs = Column(JSON, nullable=True)
    max_inter_gs_hd = Column(Integer, nullable=True)
