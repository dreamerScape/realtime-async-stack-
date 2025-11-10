from fastapi import FastAPI,Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from db.session import get_db_session

from redis.asyncio import Redis
from db.redis_conn import get_redis_client
from services import cashe_service

from shemas.poll import PollCreate, Poll as PollSchema, Option as OptionSchema, VoteCreate
from services import poll_service
app = FastAPI(title="Real-time Async Stack")

# @app.get("/")
# def read_root(db: AsyncSession = Depends(get_db_session)):
#     return {"status": "ok", "db_connection": "successful"}

@app.post("/polls/{poll_id}/vote", status_code=status.HTTP_202_ACCEPTED)
async def vote_on_poll_endpoint(
    poll_id: int,
    vote_data: VoteCreate,
    response: Response,
    redis: Redis = Depends(get_redis_client),
    
):
    
    await poll_service.add_vote(redis, poll_id, vote_data)
    
    return {"message": "Vote accepted for processing"}
    

@app.get("/polls/{poll_id}", response_model = PollSchema)
async def get_poll_endpoint(
    poll_id: int,
    db: AsyncSession = Depends(get_db_session),
    redis: Redis = Depends(get_redis_client)
):
    cashed_poll = await cashe_service.get_poll_from_cache(poll_id, redis)
    if cashed_poll:
        return cashed_poll
    
    poll = await poll_service.get_poll(db, poll_id)
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    
    poll_schema = PollSchema.model_validate(poll)
    await cashe_service.set_poll_to_cashe(poll_schema, redis)
    
    
    return poll_schema
     

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
    