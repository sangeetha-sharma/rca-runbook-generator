"""initial empty schema

Revision ID: 7b86a21a2b66
Revises:
Create Date: 2026-07-27 10:23:24.184038

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "7b86a21a2b66"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
