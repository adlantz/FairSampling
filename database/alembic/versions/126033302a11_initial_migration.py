"""Initial migration

Revision ID: 126033302a11
Revises: 
Create Date: 2024-05-22 12:53:10.726513

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '126033302a11'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('instances_N8',
    sa.Column('seed', sa.Integer(), nullable=False),
    sa.Column('Jij_matrix', sa.JSON(), nullable=False),
    sa.Column('ground_states', sa.JSON(), nullable=False),
    sa.PrimaryKeyConstraint('seed')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('instances_N8')
    # ### end Alembic commands ###
