from sqlalchemy.ext.asyncio import AsyncSession
from shemas.poll import PollCreate, VoteCreate
from models.poll import Poll
from repositories import poll_repo

async def create_new_poll(db: AsyncSession, poll_data: PollCreate) -> Poll:
    #.... buisness logic can be added here ...
    return await poll_repo.create_poll(db, poll_data)

async def get_poll(db: AsyncSession, poll_id: int) -> Poll:
    #.... buisness logic can be added here ...
    return await poll_repo.get_poll_by_id(db, poll_id)

async def add_vote(db: AsyncSession, poll_id: int, vote_data: VoteCreate):
    #.... buisness logic can be added here ...
    
    updated_opiton = await poll_repo.add_vote_to_option(
        db=db,
        poll_id=poll_id,
        option_id=vote_data.option_id
    )
    
    return updated_opiton
