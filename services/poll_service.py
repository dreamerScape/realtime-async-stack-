from sqlalchemy.ext.asyncio import AsyncSession
from shemas.poll import PollCreate, VoteCreate
from models.poll import Poll
from repositories import poll_repo

from redis.asyncio import Redis
from services import broker_service

async def create_new_poll(db: AsyncSession, poll_data: PollCreate) -> Poll:
    #.... buisness logic can be added here ...
    return await poll_repo.create_poll(db, poll_data)

async def get_poll(db: AsyncSession, poll_id: int) -> Poll:
    #.... buisness logic can be added here ...
    return await poll_repo.get_poll_by_id(db, poll_id)

async def add_vote(redis: Redis, poll_id: int, vote_data: VoteCreate) -> None:
    #.... buisness logic can be added here ...
    
    await broker_service.publish_vote_event(
        redis=redis,
        poll_id=poll_id,
        option_id=vote_data.option_id
    )
    
    return None
