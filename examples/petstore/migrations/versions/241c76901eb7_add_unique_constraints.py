"""add unique constraints

Revision ID: 241c76901eb7
Revises: 36745fa33987
Create Date: 2022-01-06 09:15:55.561786

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "241c76901eb7"
down_revision = "36745fa33987"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "species", ["name"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "species", type_="unique")
    # ### end Alembic commands ###
