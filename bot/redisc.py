import redis.asyncio as redis
from redis.client import Redis
import config

rd = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    username=config.REDIS_USERNAME,
    password=config.REDIS_PASSWORD
)  # type: Redis
