"""Remove unique constraint in animal name field

Revision ID: edc8768cf681
Revises: 1e3cf582615c
Create Date: 2021-12-26 03:29:43.872150

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "edc8768cf681"
down_revision = "1e3cf582615c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("animal_name_key", "animal", type_="unique")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("animal_name_key", "animal", ["name"])
    # ### end Alembic commands ###
