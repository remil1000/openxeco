"""empty message

Revision ID: 54992185f712
Revises: c003c56cd46a
Create Date: 2021-12-09 15:48:43.423427

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '54992185f712'
down_revision = 'c003c56cd46a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('User', 'vcard', Boolean(name=op.f('ck_bool_t_x')))


def downgrade():
    op.drop_column('User', 'vcard')
