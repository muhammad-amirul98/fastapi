"""add content column to posts table

Revision ID: 3780e1882810
Revises: f96abd3aa8a2
Create Date: 2023-11-17 14:14:45.965586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3780e1882810'
down_revision: Union[str, None] = 'f96abd3aa8a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
