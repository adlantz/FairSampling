"""add reduced gs column

Revision ID: 55862f48054f
Revises: db714ba755ae
Create Date: 2024-05-22 15:40:48.539722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55862f48054f'
down_revision: Union[str, None] = 'db714ba755ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('instances_N8', sa.Column('reduced_gs', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('instances_N8', 'reduced_gs')
    # ### end Alembic commands ###
