from pyrogram import Client
import config as V
from bot import Notices
from bot.services.mongodb import MongoSession
from bot.services.scheduler import scheduler


async def test():
    async with Client('pyro', api_id=V.API_ID, api_hash=V.API_HASH,
                      bot_token=V.BOT_TOKEN, ) as client, Notices() as notices:
        client: Client = client
        mongo = MongoSession(V.MONGO_SRV)
        async for i in mongo.user_iter():
            print(i)
        await scheduler(client, mongo, notices, )


if __name__ == '__main__':
    import asyncio

    asyncio.new_event_loop().run_until_complete(test())
