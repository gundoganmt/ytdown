"""empty message

Revision ID: 79e8f3ebaf11
Revises: 88f5db6a131c
Create Date: 2022-01-01 18:08:36.988499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79e8f3ebaf11'
down_revision = '88f5db6a131c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Admin', sa.Column('profile_picture', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Admin', 'profile_picture')
    # ### end Alembic commands ###
