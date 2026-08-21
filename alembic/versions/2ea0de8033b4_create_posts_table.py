"""create posts table

Revision ID: 2ea0de8033b4
Revises: 
Create Date: 2026-08-20 19:42:37.816519

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ea0de8033b4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean, nullable=False, server_default='TRUE'))

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
