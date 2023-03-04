import sqlalchemy as sa

from sqlalchemy.sql import func

metadata = sa.MetaData()

events_table = sa.Table(
    'events',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('title', sa.String(255), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('coordinates', sa.String()),
    sa.Column('is_active', sa.Boolean, server_default='t'),
    sa.Column('start_at', sa.DateTime(timezone=True)),
    sa.Column('end_at', sa.DateTime(timezone=True)),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
    sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now()),
)
