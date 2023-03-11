from fastapi import APIRouter, status, Depends, Response
from fastapi_pagination import paginate, Page

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import EventBase, UpdateEvent, Event
from src.models import Events, get_session


router = APIRouter(
    tags=["Events"],
    prefix="/events",
)


@router.get("/{event_id}/")
async def get_event_by_id(
    event_id: int, session: AsyncSession = Depends(get_session)
) -> Event:
    result = await Events.get_event(event_id=event_id, session=session)
    if result:
        return result
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/", response_model=Page[Event])
async def get_events(session: AsyncSession = Depends(get_session)):
    return paginate(await Events.get_all_events(session=session))


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def insert_event(event: EventBase, session: AsyncSession = Depends(get_session)):
    return await Events.add_event(event=event, session=session)


@router.put("/{event_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def put_event(
    event_id: int,
    update_data: UpdateEvent,
    session: AsyncSession = Depends(get_session),
):
    return await Events.update_event(
        event_id=event_id, update_data=update_data, session=session
    )


@router.delete("/{event_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event_by_id(
    event_id: int, session: AsyncSession = Depends(get_session)
):
    return await Events.delete_event(event_id, session)
