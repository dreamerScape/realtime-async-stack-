from sqlalchemy.ext.asyncio import AsyncSession
from models.poll import Poll, Option
from shemas.poll import PollCreate, OptionCreate
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select

async def create_poll(db: AsyncSession, poll_data: PollCreate) -> Poll:
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