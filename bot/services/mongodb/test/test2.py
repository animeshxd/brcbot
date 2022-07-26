import asyncio

from bot.services.mongodb.core import MongoSession
from config import MONGO_SRV


async def test2():
    session = MongoSession(MONGO_SRV)
    async for i in session.user_iter(subscribed=True, stopped=False, notified=False):
        print(i)

if __name__ == '__main__':
    asyncio.new_event_loop().run_until_complete(test2())