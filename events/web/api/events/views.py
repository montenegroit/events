from fastapi import APIRouter, status, Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession

from events.schemas.events import CreateEvent, EventBase, UpdateEvent, EventList
from events.db.crud import events as crud_events
from events.db.base import get_session

router = APIRouter(
    tags=['Events'],
    prefix='/events',
)


# @router.get('/',
#             response_model=EventList)
# async def get_all_events(session: AsyncSession = Depends(get_session)):
#     result = await crud_events.get_all_events(session)
#     return {'results': result}


@router.get('/{event_id}', response_model=CreateEvent)
async def get_event_by_id(event_id: int, session: AsyncSession = Depends(get_session)
    ):
    result = await crud_events.get_event(event_id, session)
    if result:
        response_object = {
            "id": result.id,
            "title": result.title,
            "description": result.description,
            "is_active": result.is_active,
            "created_at": result.created_at,
            "coordinates": result.coordinates,
            "start_at": result.start_at,
            "end_at": result.end_at,
            "updated_at": result.updated_at,
        }
        return response_object
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.post(
        '/add_event',
        status_code=status.HTTP_201_CREATED,
        response_model=CreateEvent,
        responses={
            status.HTTP_201_CREATED: {'model': CreateEvent},
            status.HTTP_400_BAD_REQUEST: {'description': 'An error occured'},
        })
async def insert_event(event: EventBase, session: AsyncSession = Depends(get_session)):
    result = await crud_events.add_event(event, session)
    return Response(status_code=status.HTTP_201_CREATED)


@router.delete(
    '/delete/{event_id}'
)
async def delete_event_by_id(
    event_id: int,
    session: AsyncSession = Depends(get_session)
) -> Response:
    result = await crud_events.delete_event(event_id, session)
    print(result)
    if result:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.patch('/{event_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_event(
    event_id: int,
    update_data: UpdateEvent,
    session: AsyncSession = Depends(get_session)
) -> Response:
    result = await crud_events.update_event(event_id, update_data, session)
    if result:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_400_BAD_REQUEST)
    



