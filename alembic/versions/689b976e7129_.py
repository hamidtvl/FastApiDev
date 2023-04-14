"""add foreign key to post table

Revision ID: 689b976e7129
Revises: 533ffe729f32
Create Date: 2023-04-14 15:23:52.874482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '689b976e7129'
down_revision = '533ffe729f32'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk',source_table='posts',referent_table='users',local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk',table_name='posts')
    op.drop_column('posts','owner_id')
    pass
