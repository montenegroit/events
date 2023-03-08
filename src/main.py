import uvicorn
from fastapi import FastAPI

from . import view



app = FastAPI(
    title="events",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)
app.include_router(view.router)


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000,
    )
