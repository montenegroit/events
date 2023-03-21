from fastapi import FastAPI
from fastapi_pagination import add_pagination
import sentry_sdk

from . import view

sentry_sdk.init(
    dsn="https://0f3c1cc149a0488e9c57e5c7ef692697@o4504875436539904.ingest.sentry.io/4504875437588480",
    traces_sample_rate=1.0,
)

app = FastAPI(
    title="events",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)
app.include_router(view.router)

add_pagination(app)
