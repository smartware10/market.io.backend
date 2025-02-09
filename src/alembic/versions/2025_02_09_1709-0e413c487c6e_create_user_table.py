"""Create user table

Revision ID: 0e413c487c6e
Revises: 947085d8a9ed
Create Date: 2025-02-09 17:09:15.024659

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0e413c487c6e"
down_revision: Union[str, None] = "947085d8a9ed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("email", sa.String(length=320), nullable=False))
    op.add_column(
        "users", sa.Column("hashed_password", sa.String(length=1024), nullable=False)
    )
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=False))
    op.add_column("users", sa.Column("is_superuser", sa.Boolean(), nullable=False))
    op.add_column("users", sa.Column("is_verified", sa.Boolean(), nullable=False))
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_column("users", "is_verified")
    op.drop_column("users", "is_superuser")
    op.drop_column("users", "is_active")
    op.drop_column("users", "hashed_password")
    op.drop_column("users", "email")
