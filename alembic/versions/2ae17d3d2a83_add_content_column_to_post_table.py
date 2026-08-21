"""add content column to post table

Revision ID: 2ae17d3d2a83
Revises: 2ea0de8033b4
Create Date: 2026-08-20 20:28:34.685596

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ae17d3d2a83'
down_revision: Union[str, Sequence[str], None] = '2ea0de8033b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
