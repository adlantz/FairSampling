"""initialize

Revision ID: 21dc92e6ece7
Revises: 
Create Date: 2025-06-29 15:15:53.249866

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "21dc92e6ece7"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "instance",
        sa.Column("N", sa.Integer(), nullable=False),
        sa.Column("seed", sa.Integer(), nullable=False),
        sa.Column("jij_matrix", sa.JSON(), nullable=True),
        sa.Column("bonds", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("N", "seed"),
    )
    op.create_table(
        "instancegroundstates",
        sa.Column("N", sa.Integer(), nullable=False),
        sa.Column("seed", sa.Integer(), nullable=False),
        sa.Column("ground_states", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("N", "seed"),
    )
    op.create_table(
        "instancepostannealinginfo",
        sa.Column("N", sa.Integer(), nullable=False),
        sa.Column("seed", sa.Integer(), nullable=False),
        sa.Column("gs_amplitudes", sa.JSON(), nullable=True),
        sa.Column("suppression_ratio", sa.Float(), nullable=True),
        sa.Column("diag_run_h_array", sa.JSON(), nullable=True),
        sa.Column("diag_run_fidelities", sa.JSON(), nullable=True),
        sa.Column("diag_run_e_gaps", sa.JSON(), nullable=True),
        sa.Column("diag_run_failure", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("N", "seed"),
    )
    op.create_table(
        "job",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("params", sa.JSON(), nullable=True),
        sa.Column("status", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("job")
    op.drop_table("instancepostannealinginfo")
    op.drop_table("instancegroundstates")
    op.drop_table("instance")
    # ### end Alembic commands ###
