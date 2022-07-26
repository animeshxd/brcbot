import logging
import typing

from pyrogram.types import User

from bot.services.mongodb.classes import MUser
from bot.services.mongodb.core._MongoSession import _MongoSession


class _UsersMongo(_MongoSession):

    async def user_subscribe(self, user_id: int):
        return await self.users.update_one({'_id': user_id}, {'$set': {'subscribed': True}}, upsert=True)

    async def user_unsubscribe(self, user_id: int):
        return await self.users.update_one({'_id': user_id}, {'$set': {'subscribed': False}}, upsert=True)

    async def user_add(self, _id: int):
        return await self.user_update(_id, False, False, False)

    async def user_update(self,
                          _id: int,
                          stopped: bool = None,
                          subscribed: bool = None,
                          notified: bool = None,
                          id: int = None
                          ):
        data = {'_id': _id, 'stopped': stopped, 'subscribed': subscribed, 'notified': notified}
        x = {k: v for k, v in data.items() if v is not None}
        logging.info(f'update/insert: {x}')
        return await self.users.update_one({'_id': _id}, {'$set': x}, upsert=True)

    async def user_find(self, user: typing.Union[int, User]):
        found = await self.users.find_one({'_id': user}, {})
        if not found:
            return None
        return MUser(**found)

    async def user_iter(self, subscribed: bool = True, stopped: bool = False, notified: bool = False):
        async for i in self.users.find({'subscribed': subscribed, 'stopped': stopped, 'notified': notified}):
            yield MUser(**i)
