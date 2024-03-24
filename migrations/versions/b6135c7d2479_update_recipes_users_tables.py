"""update recipes & users tables

Revision ID: b6135c7d2479
Revises: a3de39dd5863
Create Date: 2024-03-21 22:00:30.144825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6135c7d2479'
down_revision = 'a3de39dd5863'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_approved', sa.Boolean(), nullable=True))

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_admin', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('is_admin')

    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.drop_column('is_approved')

    # ### end Alembic commands ###