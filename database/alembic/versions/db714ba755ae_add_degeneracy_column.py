"""add degeneracy column

Revision ID: db714ba755ae
Revises: 126033302a11
Create Date: 2024-05-22 15:20:35.366131

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db714ba755ae'
down_revision: Union[str, None] = '126033302a11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('instances_N8', sa.Column('degeneracy', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('instances_N8', 'degeneracy')
    # ### end Alembic commands ###
