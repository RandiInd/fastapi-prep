"""create posts table

Revision ID: 0ed6e226b982
Revises: 
Create Date: 2022-05-18 11:46:26.400855

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ed6e226b982'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():  # when we run upgrade need put those commands to upgrade
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                             sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade(): # if we want to rollback things done then need to put into downgrade
    op.drop_table('posts')
    pass

