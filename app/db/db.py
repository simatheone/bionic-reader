from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.db.settings import settings

engine = create_async_engine(settings.database_url)


async def get_async_session():
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)
    async with AsyncSessionLocal() as async_session:
        yield async_session
