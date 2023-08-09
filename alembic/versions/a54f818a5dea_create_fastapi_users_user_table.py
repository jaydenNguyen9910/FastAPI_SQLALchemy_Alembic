"""create FastAPI Users User table

Revision ID: a54f818a5dea
Revises: 
Create Date: 2023-08-07 19:16:08.382796

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from fastapi_users_db_sqlalchemy import GUID

# revision identifiers, used by Alembic.
revision: str = 'a54f818a5dea'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(  # This tells Alembic that, when upgrading, a table needs to be created.
        "user",  # The name of the table.
        sa.Column("id", GUID, primary_key=True),  # The column "id" uses the custom type imported earlier.
        sa.Column(
            "email", sa.String(length=320), unique=True, index=True, nullable=False
        ),
        sa.Column("hashed_password", sa.String(length=72), nullable=False),
        sa.Column("is_active", sa.Boolean, default=True, nullable=False),
        sa.Column("is_superuser", sa.Boolean, default=False, nullable=False),
        sa.Column("is_verified", sa.Boolean, default=False, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("user")
