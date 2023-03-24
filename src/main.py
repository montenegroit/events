import os
import sentry_sdk
import uvicorn

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from dotenv import load_dotenv

from . import view
from src.schemas import settings

load_dotenv()

sentry_sdk.init(
    dsn=settings.sentry_sdk,
    traces_sample_rate=1.0,
)

app = FastAPI(
    title="events",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)
app.include_router(view.router)

add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="localhost",
        port=8000,
    )
