import asyncio
import pytest
import pytest_asyncio

from httpx import AsyncClient
from fastapi import status
from datetime import datetime, timezone

from src.main import app


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def get_app():
    async with AsyncClient(app=app, base_url="http://127.0.0.1") as client:
        yield client


@pytest.mark.asyncio
class TestsEndpoints:
    async def test_smoke_get_events(self, get_app):
        response = await get_app.get("/events/")
        assert response.status_code == status.HTTP_200_OK

    async def test_smoke_get_event_by_id(self, get_app):
        response = await get_app.get("/events/6/")
        assert response.status_code == status.HTTP_200_OK

    async def test_smoke_post_event(self, get_app):
        data = {
            "title": "string",
            "description": "string",
            "is_active": True,
            "created_at": str(datetime.now(timezone.utc)),
            "coordinates": "string",
            "start_at": str(datetime.now(timezone.utc)),
            "end_at": str(datetime.now(timezone.utc)),
        }
        headers = {"Content-Type": "application/json"}
        response = await get_app.post("/events/", json=data, headers=headers)
        assert response.status_code == status.HTTP_201_CREATED

    async def test_smoke_delete_event(self, get_app):
        response = await get_app.delete("/events/1/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_smoke_put_request_event(self, get_app):
        data = {
            "title": "string",
            "description": "PUT TESTS",
            "is_active": True,
            "created_at": str(datetime.now(timezone.utc)),
            "coordinates": "string",
            "start_at": str(datetime.now(timezone.utc)),
            "end_at": str(datetime.now(timezone.utc)),
            "updated_at": str(datetime.now(timezone.utc)),
        }
        headers = {"Content-Type": "application/json"}
        response = await get_app.put("/events/6/", json=data, headers=headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT
