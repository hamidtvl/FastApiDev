"""create posts table

Revision ID: 91526b90d7fd
Revises: 
Create Date: 2023-04-13 19:25:00.896704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91526b90d7fd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
