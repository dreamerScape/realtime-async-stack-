from sqlalchemy.ext.asyncio import AsyncSession
from models.poll import Poll, Option
from shemas.poll import PollCreate, OptionCreate

async def create_poll(db: AsyncSession, poll_data: PollCreate) -> Poll:
    db_poll = Poll(question=poll_data.question)
    
    db.add(db_poll)
    
    await db.flush()
    
    db_options = [
        Option(text=opt.text, poll_id=db_poll.id)
        for opt in poll_data.options
    ]
    
    db.add_all(db_options)
    
    db_poll.options = db_options
    
    await db.commit()
    
    # await db.refresh(db_poll)
    
    return db_poll