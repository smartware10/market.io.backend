"""Reset DB

Revision ID: b7d6a9bd7b1b
Revises: 3be92f12e673
Create Date: 2025-02-11 13:15:40.563763

"""

from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b7d6a9bd7b1b"
down_revision: Union[str, None] = "3be92f12e673"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.String(length=1024), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_table(
        "accesstokens",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token", sa.String(length=43), nullable=False),
        sa.Column(
            "created_at",
            fastapi_users_db_sqlalchemy.generics.TIMESTAMPAware(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_accesstokens_user_id_users"),
            ondelete="cascade",
        ),
        sa.PrimaryKeyConstraint("token", name=op.f("pk_accesstokens")),
    )
    op.create_index(
        op.f("ix_accesstokens_created_at"), "accesstokens", ["created_at"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_accesstokens_created_at"), table_name="accesstokens")
    op.drop_table("accesstokens")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
