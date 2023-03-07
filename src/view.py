from fastapi import APIRouter, status, Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import CreateEvent, EventBase, EventList, UpdateEvent
from src.models import (
    get_session, get_event, add_event, get_all_events, delete_event, update_event
)


router = APIRouter(
    tags=['Events'],
    prefix='/events',
)


@router.get('/{event_id}')
async def get_event_by_id(event_id: int, session: AsyncSession = Depends(get_session)
    ):
    result = await get_event(event_id=event_id, session=session)
    if result:
        return result
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/',
            response_model=EventList)
async def get_events(session: AsyncSession = Depends(get_session)):
    results = await get_all_events(session=session)
    for row in range(len(results)):
        results[row] = results[row]._asdict()
    return {'results': results}


@router.post(
        '/',
        status_code=status.HTTP_201_CREATED,
        response_model=CreateEvent,
)
async def insert_event(event: EventBase, session: AsyncSession = Depends(get_session)):
    await add_event(event=event, session=session)
    return Response(status_code=status.HTTP_201_CREATED)


@router.put('/{event_id}', status_code=status.HTTP_204_NO_CONTENT)
async def put_event(
    event_id: int,
    update_data: UpdateEvent,
    session: AsyncSession = Depends(get_session)
) -> Response:
    await update_event(
        event_id=event_id,
        update_data=update_data,
        session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    '/{event_id}'
)
async def delete_event_by_id(
    event_id: int,
    session: AsyncSession = Depends(get_session)
) -> Response:
    await delete_event(event_id, session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

