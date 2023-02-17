import logging
import typing
from pymongo import UpdateOne

from pymongo.results import UpdateResult, BulkWriteResult
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

    async def user_add_bulk(self, users: typing.Iterable[int],
                            stopped: bool = None,
                            subscribed: bool = None,
                            notified: bool = None,) -> BulkWriteResult:
        data = {'stopped': stopped,
                'subscribed': subscribed, 'notified': notified}
        x = {k: v for k, v in data.items() if v is not None}
        return await self.users.bulk_write(
            [
                UpdateOne({'_id': i}, {'$set': {'_id': i} | x}, upsert=True) for i in users
            ]
        )

    async def user_update(self,
                          _id: int,
                          stopped: bool = None,
                          subscribed: bool = None,
                          notified: bool = None,
                          id: int = None
                          ) -> UpdateResult:
        if id:
            _id = id
        data = {'_id': _id, 'stopped': stopped,
                'subscribed': subscribed, 'notified': notified}
        x = {k: v for k, v in data.items() if v is not None}
        # logging.debug(f'update/insert: {{{_id}: {x}}}')
        return await self.users.update_one({'_id': _id}, {'$set': x}, upsert=True)

    async def user_update_many(self, users: list[int], stopped: bool = None, subscribed: bool = None, notified: bool = None):
        data = {'stopped': stopped,
                'subscribed': subscribed, 'notified': notified}
        x = {k: v for k, v in data.items() if v is not None}
        return await self.users.update({'_id': {'$in': users}}, {'$set': x}, multi=True)

    async def user_find(self, user: typing.Union[int, User]):
        found = await self.users.find_one({'_id': user}, {})
        if not found:
            return None
        return MUser(**found)

    async def user_iter(self,
                        subscribed: bool = None,
                        stopped: bool = None,
                        notified: bool = None) -> typing.AsyncGenerator[MUser, None]:
        data = {'stopped': stopped,
                'subscribed': subscribed, 'notified': notified}
        x = {k: v for k, v in data.items() if v is not None}
        async for i in self.users.find(x):
            yield MUser(**i)
        return
