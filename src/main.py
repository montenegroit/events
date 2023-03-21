import os
import sentry_sdk

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from dotenv import load_dotenv

from . import view

load_dotenv()

sentry_sdk.init(
    dsn=os.getenv("sentry_sdk"),
    traces_sample_rate=1.0,
)

app = FastAPI(
    title="events",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)
app.include_router(view.router)

add_pagination(app)
