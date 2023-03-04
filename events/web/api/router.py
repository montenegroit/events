from fastapi.routing import APIRouter

from api import monitoring
from api import events

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(events.router)
