from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models import Base


engine = create_async_engine(
    "postgresql+asyncpg://asyncio_db_user:1234@127.0.0.1:5431/hw_asyncio"
)


async def get_async_session(drop: bool = False, create: bool = False):
    async with engine.begin() as connection:
        if drop:
            await connection.run_sync(Base.metadata.drop_all)
        if create:
            await connection.run_sync(Base.metadata.create_all)
    async_session_maker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker


async def create_db_session():
    await get_async_session(True, True)
