"""empty message

Revision ID: d7f3f3b73d86
Revises:
Create Date: 2022-04-07 21:50:11.693957

"""
# flake8: noqa: E122

import sqlalchemy as sa
import sqlmodel.sql.sqltypes

from alembic import op
from app.db.process import seed_db


# revision identifiers, used by Alembic.
revision = 'd7f3f3b73d86'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('airport',
    sa.Column('iata', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('country_code', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('iata')
    )
    op.create_index(op.f('ix_airport_iata'), 'airport', ['iata'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_airport_iata'), table_name='airport')
    op.drop_table('airport')
