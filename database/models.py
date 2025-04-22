from sqlalchemy import Column, Integer, JSON, REAL, Boolean, PrimaryKeyConstraint
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
    post_anneal_overlap_dist = Column(JSON, nullable=True)
    post_anneal_od_mean = Column(REAL, nullable=True)
    post_anneal_od_variance = Column(REAL, nullable=True)

    # Diagonalization info
    diag_run_h_array = Column(JSON, nullable=True)
    diag_run_fidelities = Column(JSON, nullable=True)
    diag_run_e_gaps = Column(JSON, nullable=True)
    diag_run_failure = Column(Boolean, nullable=True)

    # Macroscopic quantumness measures
    disc_fair_sampling = Column(Integer, nullable=True)
    disc_post_anneal = Column(Integer, nullable=True)
    qfi_fair_sampling = Column(Integer, nullable=True)
    qfi_post_anneal = Column(Integer, nullable=True)
    dist_fair_sampling = Column(Integer, nullable=True)
    dist_post_anneal = Column(Integer, nullable=True)

    # Macroscopic measures full gs
    full_gs_od_variance = Column(REAL, nullable=True)
    full_gs_post_anneal_od_variance = Column(REAL, nullable=True)
    full_gs_qfi_fair_sampling = Column(Integer, nullable=True)
    full_gs_qfi_post_anneal = Column(Integer, nullable=True)

    full_post_anneal_gs_probs = Column(JSON, nullable=True)


class InstancesN12(Base):
    __tablename__ = "instances_N12"
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
    post_anneal_overlap_dist = Column(JSON, nullable=True)
    post_anneal_od_mean = Column(REAL, nullable=True)
    post_anneal_od_variance = Column(REAL, nullable=True)

    # Diagonalization info
    diag_run_h_array = Column(JSON, nullable=True)
    diag_run_fidelities = Column(JSON, nullable=True)
    diag_run_e_gaps = Column(JSON, nullable=True)
    diag_run_failure = Column(Boolean, nullable=True)

    # Macroscopic quantumness measures
    disc_fair_sampling = Column(Integer, nullable=True)
    disc_post_anneal = Column(Integer, nullable=True)
    qfi_fair_sampling = Column(Integer, nullable=True)
    qfi_post_anneal = Column(Integer, nullable=True)
    dist_fair_sampling = Column(Integer, nullable=True)
    dist_post_anneal = Column(Integer, nullable=True)

    # Macroscopic measures full gs
    full_gs_od_variance = Column(REAL, nullable=True)
    full_gs_post_anneal_od_variance = Column(REAL, nullable=True)
    full_gs_qfi_fair_sampling = Column(Integer, nullable=True)
    full_gs_qfi_post_anneal = Column(Integer, nullable=True)

    full_post_anneal_gs_probs = Column(JSON, nullable=True)


class InstancesN16(Base):
    __tablename__ = "instances_N16"
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
    post_anneal_overlap_dist = Column(JSON, nullable=True)
    post_anneal_od_mean = Column(REAL, nullable=True)
    post_anneal_od_variance = Column(REAL, nullable=True)

    # Diagonalization info
    diag_run_h_array = Column(JSON, nullable=True)
    diag_run_fidelities = Column(JSON, nullable=True)
    diag_run_e_gaps = Column(JSON, nullable=True)
    diag_run_failure = Column(Boolean, nullable=True)

    # Macroscopic quantumness measures
    disc_fair_sampling = Column(Integer, nullable=True)
    disc_post_anneal = Column(Integer, nullable=True)
    qfi_fair_sampling = Column(Integer, nullable=True)
    qfi_post_anneal = Column(Integer, nullable=True)
    dist_fair_sampling = Column(Integer, nullable=True)
    dist_post_anneal = Column(Integer, nullable=True)

    # Macroscopic measures full gs
    full_gs_od_variance = Column(REAL, nullable=True)
    full_gs_post_anneal_od_variance = Column(REAL, nullable=True)
    full_gs_qfi_fair_sampling = Column(Integer, nullable=True)
    full_gs_qfi_post_anneal = Column(Integer, nullable=True)

    full_post_anneal_gs_probs = Column(JSON, nullable=True)


class LargeN(Base):
    __tablename__ = "large_n"

    size = Column(Integer, nullable=False)
    seed = Column(Integer, nullable=False)

    ground_states = Column(JSON, nullable=False)
    degeneracy = Column(Integer, nullable=True)
    reduced_gs = Column(JSON, nullable=True)

    overlap_dist = Column(JSON, nullable=True)
    od_mean = Column(REAL, nullable=True)
    od_variance = Column(REAL, nullable=True)

    n_eff = Column(Integer, nullable=True)

    __table_args__ = (PrimaryKeyConstraint("size", "seed"),)
