"""
create event table

Revision ID: 50cf60cbffe3
Revises: 
Create Date: 2023-04-28 22:07:04.321118

"""
from enum import Enum

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '50cf60cbffe3'
down_revision = None
branch_labels = None
depends_on = None


class EventState(str, Enum):
    NEW = 'new'
    FINISHED_WIN = 'finished_new'
    FINISHED_LOSE = 'finished_lose'


def upgrade() -> None:
    op.create_table(
        'event',
        sa.Column('event_id', sa.String, primary_key=True, index=True),
        sa.Column('coefficient', sa.Float),
        sa.Column('deadline', sa.DateTime),
        sa.Column('state', sa.Enum(EventState), default=EventState.NEW),
    )


def downgrade() -> None:
    op.drop_table('event')
