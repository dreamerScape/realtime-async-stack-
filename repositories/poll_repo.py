from sqlalchemy.ext.asyncio import AsyncSession
from models.poll import Poll, Option
from shemas.poll import PollCreate, OptionCreate
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from typing import Optional

async def create_poll(db: AsyncSession, poll_data: PollCreate) -> Optional[Poll]:
    db_poll = Poll(question=poll_data.question)
    
    db_options = [
        Option(text=opt.text, poll_id=db_poll.id)
        for opt in poll_data.options
    ]
    
    db_poll.options = db_options
    
    db.add(db_poll)
    
    await db.commit()
    
    await db.refresh(db_poll)
    
    query = (
        select(Poll)
        .where(Poll.id == db_poll.id)
        .options(selectinload(Poll.options))
    )
    
    result = await db.execute(query)
    
    eager_poll = result.unique().scalar_one()
    
    return eager_poll

async def get_poll_by_id(db: AsyncSession, poll_id: int ) -> Poll:
    query = select(Poll).where(Poll.id == poll_id).options(selectinload(Poll.options))
    result = await db.execute(query)
    return result.unique().scalar_one_or_none()

async def add_vote_to_option(db: AsyncSession, option_id: int, poll_id: int) -> Optional[Option]:
    query = select(Option).where(Option.id == option_id).where(Option.poll_id == poll_id)
    result = await db.execute(query)
    option_to_update = result.scalar_one_or_none()
    
    if not option_to_update:
        return None
    
    option_to_update.votes += 1
        
    await db.commit()
    
    await db.refresh(option_to_update)
    
    return option_to_update
    