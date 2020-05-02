"""empty message

Revision ID: fea65e3a1038
Revises: 04717f0a782c
Create Date: 2020-05-02 14:31:58.877619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fea65e3a1038'
down_revision = '04717f0a782c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Shows', sa.Column('artist_id', sa.Integer(), nullable=True))
    op.add_column('Shows', sa.Column('venue_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Shows', 'venue_id')
    op.drop_column('Shows', 'artist_id')
    # ### end Alembic commands ###
