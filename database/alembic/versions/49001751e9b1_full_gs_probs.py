"""full gs probs

Revision ID: 49001751e9b1
Revises: ffb9a86b1b95
Create Date: 2025-04-21 22:17:07.837311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49001751e9b1'
down_revision: Union[str, None] = 'ffb9a86b1b95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('instances_N12', sa.Column('full_post_anneal_gs_probs', sa.JSON(), nullable=True))
    op.add_column('instances_N16', sa.Column('full_post_anneal_gs_probs', sa.JSON(), nullable=True))
    op.add_column('instances_N8', sa.Column('full_post_anneal_gs_probs', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('instances_N8', 'full_post_anneal_gs_probs')
    op.drop_column('instances_N16', 'full_post_anneal_gs_probs')
    op.drop_column('instances_N12', 'full_post_anneal_gs_probs')
    # ### end Alembic commands ###
