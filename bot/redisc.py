import redis.asyncio as redis
from redis.client import Redis

rd = redis.Redis(host="localhost")  # type: Redis