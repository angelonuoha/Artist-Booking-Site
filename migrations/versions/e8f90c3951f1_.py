"""empty message

Revision ID: e8f90c3951f1
Revises: 8d62eebf6c1a
Create Date: 2020-05-03 09:42:42.455270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8f90c3951f1'
down_revision = '8d62eebf6c1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Shows', 'time',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Shows', 'time',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
