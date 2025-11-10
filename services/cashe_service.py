from redis.asyncio import Redis
from shemas.poll import Poll as PollSchema
from typing import Optional
import json

POLL_CASHE_PREFIX = "POLL:"
CASHE_TTL_SECONDS = 60 * 10
async def get_poll_from_cache(poll_id: int, redis_client: Redis) -> Optional[PollSchema]:
    cache_key = f"{POLL_CASHE_PREFIX}{poll_id}"
    
    cashed_poll = await redis_client.get(cache_key)
    
    if cashed_poll is None:
        return None
    
    poll_data = json.loads(cashed_poll)
    return PollSchema(**poll_data)

async def set_poll_to_cashe(poll: PollSchema, redis: Redis):
    cashe_key = f"{POLL_CASHE_PREFIX}{poll.id}"
    
    poll_json = poll.model_dump_json()
    
    await redis.setex(cashe_key, CASHE_TTL_SECONDS, poll_json)
    
    
    
    