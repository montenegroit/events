from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from events.schemas import events as events_schemas

from events.db.models.events import events_table


async def get_event(event_id: int, session: AsyncSession):
    result = await session.execute(events_table.select().where(
        events_table.c.id == event_id)
    )
    return result.fetchone()


async def get_all_events(session: AsyncSession):
    result = await session.execute(events_table.select())
    return result.fetchall()

async def add_event(event: events_schemas.CreateEvent, session: AsyncSession):
    result =  await session.execute(insert(events_table).values(
        **event.dict()
    ))
    await session.commit()
    return result.fetchone()


async def delete_event(event_id:int, session: AsyncSession):
    result = await session.execute(events_table.delete().where(
        events_table.c.id == event_id
    ))
    await session.commit()
    return result


async def update_event(
        event_id:int,
        update_data: events_schemas.UpdateEvent,
        session: AsyncSession):
    result = await session.execute(events_table.update().where(
        events_table.c.id == event_id
    ).values(
        id=event_id,
        **update_data.dict()
    ))
    await session.commit()
    return result
