from sqlalchemy import Column, Integer, JSON, REAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Define Python objects here that correspond to tables in the db
class InstancesN8(Base):
    __tablename__ = "instances_N8"
    # Primary key directly from Numpy.random seed used to generate instance
    seed = Column(Integer, primary_key=True)

    # Classical info
    Jij_matrix = Column(JSON, nullable=False)
    ground_states = Column(JSON, nullable=False)
    degeneracy = Column(Integer, nullable=True)
    reduced_gs = Column(JSON, nullable=True)
    max_inter_gs_hd = Column(Integer, nullable=True)
    overlap_dist = Column(JSON, nullable=True)
    od_mean = Column(REAL, nullable=True)
    od_variance = Column(REAL, nullable=True)

    # Post quantum annealing info
    post_anneal_gs_probs = Column(JSON, nullable=True)
    post_anneal_supp_ratio = Column(REAL, nullable=True)
    post_anneal_gs = Column(JSON, nullable=True)
    post_anneal_deg = Column(Integer, nullable=True)
    post_anneal_overlap_dist = Column(JSON, nullable=True)
    post_anneal_od_mean = Column(REAL, nullable=True)
    post_anneal_od_variance = Column(REAL, nullable=True)
    post_anneal_max_inter_gs_hd = Column(Integer, nullable=True)
