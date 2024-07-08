"""Added users table.

Revision ID: f3656699ed19
Revises: c68dd7883249
Create Date: 2024-07-04 23:41:27.794812

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f3656699ed19'
down_revision: Union[str, None] = 'c68dd7883249'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    op.drop_table('users')
