import logging
from dataclasses import asdict

import pymongo.results
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from pyrogram.types import User
from pyrogram.raw.types import UpdateBotStopped
import typing

from bot.services.mongodb.models import MUser
from config import MONGO_SRV


class MongoSession:
    mongo: AsyncIOMotorClient
    notices: AsyncIOMotorCollection
    users: AsyncIOMotorCollection

    def __init__(self, src: str):
        self.mongo = AsyncIOMotorClient(src)
        db: AsyncIOMotorDatabase = self.mongo['brc']
        self.notices = db['notices']
        self.users = db['users']

    async def subscribe(self, user_id: int):
        return await self.users.update_one({'_id': user_id}, {'$set': {'subscribed': True}}, upsert=True)

    async def unsubscribe(self, user_id: int):
        return await self.users.update_one({'_id': user_id}, {'$set': {'subscribed': False}}, upsert=True)

    async def update(self, user_id: int, stopped: bool = False, subscribed: bool = None):
        logging.info('update/insert: {"_id": %d, "stopped": %s, "subscribed": %s}' % (user_id, stopped, subscribed))
        update = {'stopped': stopped}
        if subscribed is not None:
            update['subscribed'] = subscribed
        return await self.users.update_one(
            {'_id': user_id}, {'$set': update}, upsert=True
        )

    async def find_user(self, user: typing.Union[int, User]):
        found = await self.users.find_one({'_id': user}, {})
        if not found:
            return None
        return MUser(*found)


if __name__ == '__main__':
    import asyncio


    async def test():
        session = MongoSession(MONGO_SRV)
        result = await session.update(124, subscribed=True)
        print(result)
        result = await session.find_user(124)
        print(result)


    asyncio.new_event_loop().run_until_complete(test())
