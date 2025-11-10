from sqlalchemy.ext.asyncio import AsyncSession
from shemas.poll import PollCreate
from models.poll import Poll
from repositories import poll_repo

async def create_new_poll(db: AsyncSession, poll_data: PollCreate) -> Poll:
    #.... buisness logic can be added here ...
    return await poll_repo.create_poll(db, poll_data)

async def get_poll(db: AsyncSession, poll_id: int) -> Poll:
    #.... buisness logic can be added here ...
    return await poll_repo.get_poll_by_id(db, poll_id)
