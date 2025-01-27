"""add N16

Revision ID: 1700085bcdc8
Revises: 874cc305661a
Create Date: 2024-08-12 14:45:42.430554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1700085bcdc8'
down_revision: Union[str, None] = '874cc305661a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('instances_N16',
    sa.Column('seed', sa.Integer(), nullable=False),
    sa.Column('Jij_matrix', sa.JSON(), nullable=False),
    sa.Column('ground_states', sa.JSON(), nullable=False),
    sa.Column('degeneracy', sa.Integer(), nullable=True),
    sa.Column('reduced_gs', sa.JSON(), nullable=True),
    sa.Column('max_inter_gs_hd', sa.Integer(), nullable=True),
    sa.Column('overlap_dist', sa.JSON(), nullable=True),
    sa.Column('od_mean', sa.REAL(), nullable=True),
    sa.Column('od_variance', sa.REAL(), nullable=True),
    sa.Column('post_anneal_gs_probs', sa.JSON(), nullable=True),
    sa.Column('post_anneal_supp_ratio', sa.REAL(), nullable=True),
    sa.Column('post_anneal_overlap_dist', sa.JSON(), nullable=True),
    sa.Column('post_anneal_od_mean', sa.REAL(), nullable=True),
    sa.Column('post_anneal_od_variance', sa.REAL(), nullable=True),
    sa.Column('diag_run_h_array', sa.JSON(), nullable=True),
    sa.Column('diag_run_fidelities', sa.JSON(), nullable=True),
    sa.Column('diag_run_e_gaps', sa.JSON(), nullable=True),
    sa.Column('diag_run_failure', sa.Boolean(), nullable=True),
    sa.Column('disc_fair_sampling', sa.Integer(), nullable=True),
    sa.Column('disc_post_anneal', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('seed')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('instances_N16')
    # ### end Alembic commands ###