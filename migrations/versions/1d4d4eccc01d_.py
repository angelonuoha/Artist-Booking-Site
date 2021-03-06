"""empty message

Revision ID: 1d4d4eccc01d
Revises: fea65e3a1038
Create Date: 2020-05-02 14:35:27.822599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d4d4eccc01d'
down_revision = 'fea65e3a1038'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Show_artist_id_fkey', 'Show', type_='foreignkey')
    op.drop_constraint('Show_venue_id_fkey', 'Show', type_='foreignkey')
    op.create_foreign_key(None, 'Shows', 'Venue', ['venue_id'], ['id'])
    op.create_foreign_key(None, 'Shows', 'Artist', ['artist_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Shows', type_='foreignkey')
    op.drop_constraint(None, 'Shows', type_='foreignkey')
    op.create_foreign_key('Show_venue_id_fkey', 'Show', 'Venue', ['venue_id'], ['id'])
    op.create_foreign_key('Show_artist_id_fkey', 'Show', 'Artist', ['artist_id'], ['id'])
    # ### end Alembic commands ###
