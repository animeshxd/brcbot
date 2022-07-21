import asyncio
import typing

from pyrogram.types import Message


class Cache:
    def __init__(self):
        self._db: typing.Dict[int, typing.List[int]] = {}
        self._one_db: typing.Dict[int, Message] = {}
        self._lock = asyncio.Lock()

    async def __call__(self, func: typing.Awaitable):
        message = await func
        await self.safe_insert(message)
        return message

    async def safe_insert(self, message: Message):
        # logging.info(f'inserted {message.chat.id} -> {message.id}')
        async with self._lock:
            data = self._db.get(message.chat.id, [])
            if data:
                data.append(message.id)
            else:
                self._db[message.chat.id] = [message.id]

    async def takeout(self, user: int):
        async with self._lock:
            data = self._db.get(user, 0)
            if data:
                pop = self._db.pop(user)
                # logging.info(f'popped {pop}')
                return pop

    async def one(self, func: typing.Awaitable):
        message: Message = await func
        async with self._lock:
            self._one_db[message.chat.id] = message
        return message

    async def take_1(self, chat_id):
        async with self._lock:
            return self._one_db.pop(chat_id, None)
