"""created_at users table.

Revision ID: a7d9d91d4710
Revises: f3656699ed19
Create Date: 2024-07-04 23:55:03.300668

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a7d9d91d4710'
down_revision: Union[str, None] = 'f3656699ed19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('created_at', sa.DateTime(timezone=True), nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'created_at')
