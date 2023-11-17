"""add user table

Revision ID: 661c222e73ba
Revises: 3780e1882810
Create Date: 2023-11-17 14:18:43.097925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '661c222e73ba'
down_revision: Union[str, None] = '3780e1882810'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", 
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False), 
                    sa.Column("password", sa.String(), nullable=False), 
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), 
                            server_default=sa.text("now()"), nullable=False), 
                    sa.PrimaryKeyConstraint("id"), 
                    sa.UniqueConstraint("email"))
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
