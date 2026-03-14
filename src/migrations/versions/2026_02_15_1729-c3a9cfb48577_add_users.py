"""add users

Revision ID: c3a9cfb48577
Revises: 64461b444cf2
Create Date: 2026-02-15 17:29:54.543437

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c3a9cfb48577"
down_revision: Union[str, Sequence[str], None] = "64461b444cf2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("passwod", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
