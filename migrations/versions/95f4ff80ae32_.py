"""empty message

Revision ID: 95f4ff80ae32
Revises: 3eb4a4a75ab4
Create Date: 2020-05-01 20:52:45.912101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95f4ff80ae32'
down_revision = '3eb4a4a75ab4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('artist_id', sa.Integer(), nullable=False))
    op.add_column('Show', sa.Column('venue_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'Show', 'Venue', ['venue_id'], ['id'])
    op.create_foreign_key(None, 'Show', 'Artist', ['artist_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Show', type_='foreignkey')
    op.drop_constraint(None, 'Show', type_='foreignkey')
    op.drop_column('Show', 'venue_id')
    op.drop_column('Show', 'artist_id')
    # ### end Alembic commands ###
