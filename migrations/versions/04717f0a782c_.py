"""empty message

Revision ID: 04717f0a782c
Revises: 61d7b10acdb7
Create Date: 2020-05-02 14:30:06.640150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04717f0a782c'
down_revision = '61d7b10acdb7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Shows')
    # ### end Alembic commands ###
