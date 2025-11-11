import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")



engine= create_async_engine(url=DATABASE_URL, echo=True)


SYNC_DATABASE_URL = os.environ.get("SYNC_DATABASE_URL")
sync_engine = create_engine(SYNC_DATABASE_URL)
SyncSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=sync_engine
)

SesionLocal = sessionmaker(
     
    bind=engine,
    class_=AsyncSession
    
)
async def get_db_session():
    async with SesionLocal() as session:
        try:
            yield session
        finally:
            await session.close()