import os
import redis.asyncio as aioredis
from redis.asyncio import Redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_pool = aioredis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
    decode_responses=True
)

async def get_redis_client():
    async with aioredis.Redis(connection_pool=redis_pool) as redis_client:
        try:
            yield redis_client
        finally:
            pass
        
