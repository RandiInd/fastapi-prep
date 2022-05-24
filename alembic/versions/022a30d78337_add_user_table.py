"""add user table

Revision ID: 022a30d78337
Revises: 299a6f3add4b
Create Date: 2022-05-18 12:55:56.255783

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '022a30d78337'
down_revision = '299a6f3add4b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False), 
                             sa.Column('email', sa.String(), nullable=False),
                             sa.Column('password', sa.String(), nullable=False),
                             sa.Column('created_ata', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                             sa.PrimaryKeyConstraint('id'),
                             sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
