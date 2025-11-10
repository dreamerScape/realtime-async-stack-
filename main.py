from fastapi import FastAPI,Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from db.session import get_db_session

from shemas.poll import PollCreate, Poll as PollSchema
from services import poll_service
app = FastAPI(title="Real-time Async Stack")

# @app.get("/")
# def read_root(db: AsyncSession = Depends(get_db_session)):
#     return {"status": "ok", "db_connection": "successful"}

@app.get("/polls/{poll_id}", response_model=PollSchema)
async def get_poll_endpoint(
    poll_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    poll = await poll_service.get_poll(db, poll_id)
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    
    return poll
     

@app.post("/polls", response_model=PollSchema)
async def create_poll_endpoint(
    poll_data: PollCreate,
    db: AsyncSession = Depends(get_db_session)
):
    try:
        new_poll = await poll_service.create_new_poll(db, poll_data)
        return new_poll
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Eror creating poll, {str(e)}") 
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")
    