import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")

engine= create_async_engine(url=DATABASE_URL, echo=True)

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