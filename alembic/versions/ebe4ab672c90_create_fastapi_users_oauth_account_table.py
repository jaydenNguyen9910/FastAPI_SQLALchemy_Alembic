"""Create FastAPI Users Oauth Account table

Revision ID: ebe4ab672c90
Revises: a54f818a5dea
Create Date: 2023-08-08 23:35:05.966181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from fastapi_users_db_sqlalchemy import GUID


# revision identifiers, used by Alembic.
revision: str = 'ebe4ab672c90'
down_revision: Union[str, None] = 'a54f818a5dea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(  # This tells Alembic that, when upgrading, a table needs to be created.
        "oauth_account",  # The name of the table.
        sa.Column("id", GUID, primary_key=True),  # The column "id" uses the custom type imported earlier.
        sa.Column("oauth_name", sa.String(length=100), index=True, nullable=False),
        sa.Column("access_token", sa.String(length=1024), nullable=False),
        sa.Column("expires_at", sa.Integer, nullable=True),
        sa.Column("refresh_token", sa.String(length=1024), nullable=True),
        sa.Column("account_id", sa.String(length=320), index=True, nullable=False),
        sa.Column("account_email", sa.String(length=320), nullable=False),
        sa.Column("user_id", GUID, primary_key=True),
        sa.ForeignKeyConstraint(('user_id',), ['user.id'], ondelete="CASCADE")
    )


def downgrade() -> None:
    op.drop_table("oauth_account")
