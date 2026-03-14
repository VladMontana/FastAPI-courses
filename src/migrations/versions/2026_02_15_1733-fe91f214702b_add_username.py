"""add username

Revision ID: fe91f214702b
Revises: c3a9cfb48577
Create Date: 2026-02-15 17:33:27.883586

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "fe91f214702b"
down_revision: Union[str, Sequence[str], None] = "c3a9cfb48577"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("username", sa.String(length=16), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "username")
