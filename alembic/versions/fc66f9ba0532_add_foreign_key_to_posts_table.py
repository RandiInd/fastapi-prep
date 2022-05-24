"""add foreign key to posts table

Revision ID: fc66f9ba0532
Revises: 022a30d78337
Create Date: 2022-05-18 13:08:45.149918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc66f9ba0532'
down_revision = '022a30d78337'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", 
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE" ) # arbitarary name for forien key and


    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
