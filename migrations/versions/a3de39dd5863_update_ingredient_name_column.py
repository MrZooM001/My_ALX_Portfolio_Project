"""update ingredient name column

Revision ID: a3de39dd5863
Revises: fdf6cac44557
Create Date: 2024-03-20 13:34:44.162859

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a3de39dd5863'
down_revision = 'fdf6cac44557'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ingredients', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ingredient_name', sa.String(length=120), nullable=False))
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ingredients', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', mysql.VARCHAR(length=120), nullable=False))
        batch_op.drop_column('ingredient_name')

    # ### end Alembic commands ###