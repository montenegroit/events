import uvicorn

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from . import view


app = FastAPI(
    title="events",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)
app.include_router(view.router)

add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="localhost",
        port=8000
    )
