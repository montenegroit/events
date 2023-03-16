from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config import db_port, db_user, db_name, db_host, db_pass

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}/{db_name}"
)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


Base = declarative_base()
