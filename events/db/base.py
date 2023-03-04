import os

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from events.db.meta import meta
from dotenv import load_dotenv

load_dotenv()

db_name = os.environ.get('db_name')
db_host = os.environ.get('db_host')
db_port = os.environ.get('db_port')
db_user = os.environ.get('db_user')
db_pass = os.environ.get('db_pass')

class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta

SQALCHEMY_DATABASE_URL = (
    f'postgresql+asyncpg://{db_user}:{db_pass}@{db_host}/{db_name}'
)
engine = create_async_engine(SQALCHEMY_DATABASE_URL, echo=False)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
