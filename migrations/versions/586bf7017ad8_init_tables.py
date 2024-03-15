"""init tables

Revision ID: 586bf7017ad8
Revises: 
Create Date: 2024-03-14 17:03:15.482902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '586bf7017ad8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ingredients',
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('imgUrl', sa.Text(), nullable=False),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('measurement_units',
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('quantities',
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recipes',
    sa.Column('title', sa.String(length=120), nullable=False),
    sa.Column('imgUrl', sa.Text(), nullable=False),
    sa.Column('servings', sa.Integer(), nullable=False),
    sa.Column('readyInMinutes', sa.Integer(), nullable=False),
    sa.Column('preparationMinutes', sa.Integer(), nullable=False),
    sa.Column('cookingMinutes', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('users',
    sa.Column('username', sa.String(length=60), nullable=False),
    sa.Column('email', sa.String(length=90), nullable=False),
    sa.Column('password', sa.String(length=90), nullable=False),
    sa.Column('first_name', sa.String(length=60), nullable=True),
    sa.Column('last_name', sa.String(length=60), nullable=True),
    sa.Column('profile_image', sa.Text(), nullable=True),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('recipes_ingredients',
    sa.Column('recipe_id', sa.String(length=60), nullable=False),
    sa.Column('ingredient_id', sa.String(length=60), nullable=False),
    sa.Column('quantity', sa.String(length=60), nullable=False),
    sa.Column('unit', sa.String(length=60), nullable=False),
    sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ),
    sa.ForeignKeyConstraint(['quantity'], ['quantities.id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ),
    sa.ForeignKeyConstraint(['unit'], ['measurement_units.id'], ),
    sa.PrimaryKeyConstraint('recipe_id', 'ingredient_id')
    )
    op.create_table('steps',
    sa.Column('instruction', sa.Text(), nullable=False),
    sa.Column('recipe_id', sa.String(length=60), nullable=False),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_favorites',
    sa.Column('user_id', sa.String(length=60), nullable=False),
    sa.Column('recipe_id', sa.String(length=60), nullable=False),
    sa.Column('favorite', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'recipe_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_favorites')
    op.drop_table('steps')
    op.drop_table('recipes_ingredients')
    op.drop_table('users')
    op.drop_table('recipes')
    op.drop_table('quantities')
    op.drop_table('measurement_units')
    op.drop_table('ingredients')
    # ### end Alembic commands ###
