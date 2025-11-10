from redis.asyncio import Redis
import json

VOTE_STREAM_NAME = "vote_events"

async def publish_vote_event(poll_id: int, option_id: int, redis: Redis):
    
    event_data = {
        "poll_id": str(poll_id),
        "option_id": str(option_id)
    }
    
    await redis.xadd(
        VOTE_STREAM_NAME,
        {"event_data": json.dumps(event_data)}
    )
