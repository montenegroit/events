from typing import List
from datetime import datetime

from fastapi import HTTPException

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
    async def get_all_events(session: AsyncSession) -> List:
        query = text("""SELECT * FROM events""")
        result = await session.execute(query)
        rows = result.fetchall()
        try:
            return [row._asdict() for row in rows]
        except (OperationalError, DatabaseError, InternalError) as e:
            logger.error(e)
            raise HTTPException(status_code=422, detail="Data is not valid")

    @staticmethod
    async def get_event(event_id: int, session: AsyncSession) -> event_schemas.Event:
        query = text("SELECT * FROM events WHERE id=:event_id").bindparams(
            event_id=event_id
        )
        try:
            row = await session.execute(query)
        except (OperationalError, DatabaseError, InternalError) as e:
            logger.error(e)
            raise HTTPException(status_code=422, detail="Data is not valid")
        result = row.fetchone()
        if result:
            return result._asdict()

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
            await session.commit()
            return await Events._get_event_by_timestamp(
                created_at=event.created_at,
                session=session,
            )
        except IntegrityError as e:
            logger.error(e)
            await session.rollback()
            raise HTTPException(status_code=422, detail="Data is not valid.")

    @staticmethod
    async def delete_event(event_id: int, session: AsyncSession):
        query = text("""DELETE FROM events WHERE id=:event_id""").bindparams(
            event_id=event_id
        )
        try:
            await session.execute(query)
            return await session.commit()
        except (OperationalError, DatabaseError, InternalError) as e:
            logger.error(e)
            await session.rollback()
            raise HTTPException(status_code=422, detail="Data is not valid")

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
                is_active=:is_active,
                start_at=:start_at,
                end_at=:end_at,
                created_at=:created_at,
                updated_at=:updated_at
            WHERE id=:event_id
            """
        ).bindparams(event_id=event_id)
        try:
            await session.execute(query, update_data.dict())
            await session.commit()
            result = await Events.get_event(event_id=event_id, session=session)
            return result
        except IntegrityError as e:
            logger.error(e)
            await session.rollback()
            raise HTTPException(status_code=422, detail="Data is not valid")

    @staticmethod
    async def _get_event_by_timestamp(
        created_at: datetime,
        session: AsyncSession,
    ) -> event_schemas.Event:
        select_query = text(
            "SELECT * FROM events WHERE created_at=:created_at"
        ).bindparams(created_at=created_at)
        row = await session.execute(select_query)
        result = row.fetchone()
        return result._asdict()
