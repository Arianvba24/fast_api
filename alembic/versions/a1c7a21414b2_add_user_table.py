"""add user table

Revision ID: a1c7a21414b2
Revises: f3d16737ea49
Create Date: 2025-04-20 15:39:39.558733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1c7a21414b2'
down_revision: Union[str, None] = 'f3d16737ea49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users",
                    sa.Column("id",sa.Integer(),nullable=False),
                    sa.Column("email",sa.String(),nullable=False),
                    sa.Column("password",sa.String(),nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"),nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")        
                        )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    pass
