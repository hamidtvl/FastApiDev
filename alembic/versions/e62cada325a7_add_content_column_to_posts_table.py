"""add content column to posts table

Revision ID: e62cada325a7
Revises: 91526b90d7fd
Create Date: 2023-04-13 19:38:59.646182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e62cada325a7'
down_revision = '91526b90d7fd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String,nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
