from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    DatabaseError,
    InternalError,
)

import src.schemas as event_schemas

from src.logger import logger
from src.db import Base


class Events(Base):
    __tablename__ = "events"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    title = Column(String(255), nullable=False)
    description = Column(String(), nullable=False)
    coordinates = Column(String())
    is_active = Column(Boolean, server_default="t")
    start_at = Column(TIMESTAMP(timezone=False))
    end_at = Column(TIMESTAMP(timezone=False))
    created_at = Column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=False), onupdate=func.now())

    @staticmethod
    async def get_all_events(session: AsyncSession):
        query = text("""SELECT * FROM events""")
        result = await session.execute(query)
        rows = result.fetchall()
        try:
            return [row._asdict() for row in rows]
        except Exception as e:
            logger.error(e)
            return await session.rollback()

    @staticmethod
    async def get_event(event_id: int, session: AsyncSession):
        query = text("SELECT * FROM events WHERE id=:event_id").bindparams(
            event_id=event_id
        )
        try:
            row = await session.execute(query)
        except (OperationalError, DatabaseError, InternalError) as e:
            logger.error(e)
            return await session.rollback()
        result = row.fetchone()
        if result:
            return result._asdict()
        return await session.rollback()

    @staticmethod
    async def add_event(event: event_schemas.EventBase, session: AsyncSession):
        query = text(
            """
            INSERT INTO events(title, description, coordinates, start_at,end_at,
            created_at)
            VALUES (:title, :description, :coordinates,:start_at, :end_at, :created_at)
            """
        )
        try:
            await session.execute(query, event.dict())
        except IntegrityError as e:
            logger.error(e)
            await session.rollback()
        return await session.commit()

    @staticmethod
    async def delete_event(event_id: int, session: AsyncSession):
        query = text("""DELETE FROM events WHERE id=:event_id""").bindparams(
            event_id=event_id
        )
        await session.execute(query)
        return await session.commit()

    @staticmethod
    async def update_event(
        event_id: int,
        update_data: event_schemas.UpdateEvent,
        session: AsyncSession,
    ):
        query = text(
            """
            UPDATE events
            SET title=:title,
                description=:description,
                coordinates=:coordinates,
                start_at=:start_at, end_at=:end_at,
                created_at=:created_at,
                updated_at=:updated_at
            WHERE id=:event_id
            """
        ).bindparams(event_id=event_id)
        try:
            await session.execute(query, update_data.dict())
        except IntegrityError as e:
            logger.error(e)
            await session.rollback()
        return await session.commit()
