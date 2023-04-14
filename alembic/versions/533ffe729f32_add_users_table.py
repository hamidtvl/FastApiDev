"""add users table

Revision ID: 533ffe729f32
Revises: e62cada325a7
Create Date: 2023-04-13 19:46:16.379587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '533ffe729f32'
down_revision = 'e62cada325a7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable=False),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
