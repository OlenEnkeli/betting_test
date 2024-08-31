"""
create bet table

Revision ID: 896b4f3980ae
Revises: 50cf60cbffe3
Create Date: 2023-04-30 18:07:57.616547

"""
from datetime import datetime as dt
from enum import Enum

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '896b4f3980ae'
down_revision = '50cf60cbffe3'
branch_labels = None
depends_on = None


class BetState(str, Enum):
    NEW = 'new'
    WIN = 'win'
    LOSE = 'lose'


def upgrade() -> None:
    op.create_table(
        'bet',
        sa.Column('bet_id', sa.String, primary_key=True, index=True),
        sa.Column('event_id', sa.String, sa.ForeignKey('event.event_id'), index=True),
        sa.Column('amount', sa.Float),
        sa.Column('created_at', sa.DateTime, default=dt.now),
        sa.Column('closed_at', sa.DateTime, nullable=True),
        sa.Column('state', sa.Enum(BetState), default=BetState.NEW),
    )


def downgrade() -> None:
    op.drop_table('bet')
