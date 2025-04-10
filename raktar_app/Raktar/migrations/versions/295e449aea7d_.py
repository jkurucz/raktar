"""empty message

Revision ID: 295e449aea7d
Revises: 
Create Date: 2025-03-02 14:48:42.232695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '295e449aea7d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles')
    # ### end Alembic commands ###
