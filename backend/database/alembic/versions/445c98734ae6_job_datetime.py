"""job datetime

Revision ID: 445c98734ae6
Revises: 21dc92e6ece7
Create Date: 2025-06-30 05:54:54.083577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '445c98734ae6'
down_revision: Union[str, Sequence[str], None] = '21dc92e6ece7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job', sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('job', 'submitted_at')
    # ### end Alembic commands ###
