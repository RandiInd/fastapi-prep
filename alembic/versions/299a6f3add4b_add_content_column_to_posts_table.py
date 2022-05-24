"""add content column to posts table

Revision ID: 299a6f3add4b
Revises: 0ed6e226b982
Create Date: 2022-05-18 12:43:55.371377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '299a6f3add4b'
down_revision = '0ed6e226b982'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
