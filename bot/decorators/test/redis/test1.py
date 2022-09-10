import redis.asyncio as redis
from redis.client import Redis

rd = redis.Redis(host="localhost")  # type: Redis


async def test1():
    print(await rd.set("key", "value"))
    print(await rd.get("key"))

if __name__ == '__main__':
    import asyncio
    asyncio.new_event_loop().run_until_complete(test1())