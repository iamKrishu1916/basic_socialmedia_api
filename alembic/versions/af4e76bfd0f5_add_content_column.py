"""add content column

Revision ID: af4e76bfd0f5
Revises: 53dd2f7db3dc
Create Date: 2026-02-17 18:59:17.000441

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "af4e76bfd0f5"
down_revision: Union[str, Sequence[str], None] = "53dd2f7db3dc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
