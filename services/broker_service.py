from redis.asyncio import Redis
import json

VOTE_STREAM_NAME = "vote_events"

POLL_UPDATE_CHANNEL_PREFIX = "poll_updates:"

async def publish_vote_event(poll_id: int, option_id: int, redis: Redis):
    
    event_data = {
        "poll_id": str(poll_id),
        "option_id": str(option_id)
    }
    
    await redis.xadd(
        VOTE_STREAM_NAME,
        {"event_data": json.dumps(event_data)}
    )

async def publish_real_time_update(redis: Redis, poll_id: int, message_data: str):
    channel_name = f"{POLL_UPDATE_CHANNEL_PREFIX}{poll_id}"
    
    await redis.publish(channel_name, message_data)