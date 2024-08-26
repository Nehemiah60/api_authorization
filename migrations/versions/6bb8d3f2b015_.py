"""empty message

Revision ID: 6bb8d3f2b015
Revises: 00a1b19712d3
Create Date: 2024-08-24 11:19:51.284662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bb8d3f2b015'
down_revision = '00a1b19712d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bookmark', schema=None) as batch_op:
        batch_op.alter_column('body',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('short_url',
               existing_type=sa.VARCHAR(length=3),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bookmark', schema=None) as batch_op:
        batch_op.alter_column('short_url',
               existing_type=sa.VARCHAR(length=3),
               nullable=True)
        batch_op.alter_column('body',
               existing_type=sa.TEXT(),
               nullable=True)

    # ### end Alembic commands ###
