import asyncio
import logging
import json

from db.redis_conn import redis_pool
from db.session import SesionLocal
from redis.asyncio import Redis

from services import poll_service, cashe_service, broker_service

from repositories import poll_repo

from shemas.poll import VoteCreate, Option as OptionSchema

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

STREAM_NAME = broker_service.VOTE_STREAM_NAME

GROUP_NAME = "poll_workers"

async def procees_vote_event(redis: Redis, event_data: dict):
    try:
        data = json.loads(event_data['event_data'])
        poll_id = int(data['poll_id'])
        option_id = int(data['option_id'])
        
        log.info(f"Processing vote for Poll={poll_id}, Option ={option_id}")
        
        async with SesionLocal() as db:
            vote_data = VoteCreate(option_id=option_id)
            updated_option = await poll_repo.add_vote_to_option(db, poll_id, vote_data.option_id)
            
            if not updated_option:
                log.warning(f"Option or Poll not found for Poll {poll_id}, Option {option_id}. Skipping.")
                return
        async with Redis(connection_pool=redis_pool) as redis:
            await cashe_service.clear_poll_cashe(poll_id, redis)
        
        option_shema = OptionSchema.model_validate(updated_option)
        await broker_service.publish_real_time_update(
            redis=redis,
            poll_id=poll_id,
            message_data=option_shema.model_dump_json()
        )
        log.info(f"Successfully processed vote for Poll {poll_id}, Option {option_id}")   
        
    except Exception as e:
        log.error(f"Error processing event: {e}. Data: {event_data}")
        
async def main_worker_loop():
    log.info("Starting worker loop...")   
    redis = Redis(connection_pool=redis_pool)
    
    try:
        await redis.xgroup_create(STREAM_NAME, GROUP_NAME, id="0", mkstream=True)   
        log.info(f"Consumer group '{GROUP_NAME}' created (or already exists).")
    except Exception as e:
        if "BUSYGROUP" not in str(e):
            log.error(f"Error creating consumer group: {e}")
            return
    while True:
        try:
            responce = await redis.xreadgroup(
                GROUP_NAME,
                "consumer_1",
                {STREAM_NAME: ">"},
                count=1,
                block=0
            )
            if not responce:
                continue
            
            stream, messages = responce[0]
            message_id, event_data = messages[0]
            
            await procees_vote_event(event_data)
            
            await redis.xack(STREAM_NAME, GROUP_NAME, message_id)
        
        except Exception as e:
            log.error(f"Error in worker loop: {e}")
            await asyncio.sleep(1)
            
if __name__ == "__main__":
    asyncio.run(main_worker_loop())
            
        