import asyncio
import logging
import typing


class Conversation:
    def __init__(self):
        self._dict: typing.Dict[int, typing.Optional[typing.AsyncGenerator]] = {}
        self._cp: typing.Dict[int, bool] = {}
        self._lock: asyncio.Lock = asyncio.Lock()

    async def put(self, chat_id: int, x: typing.AsyncGenerator):
        if await self.in_conversation(chat_id):
            raise RuntimeError('Already in conversation')
        async with self._lock:
            self._dict[chat_id] = x

    async def dismiss(self, chat_id: int):
        async with self._lock:
            has = self._dict.get(chat_id, False)
        if has:
            try:
                await has.aclose()
            except Exception:
                logging.exception(f"failed to dismiss conversation for user {chat_id}")
            finally:
                async with self._lock:
                    del self._dict[chat_id]

    async def in_conversation(self, chat_id: int) -> bool:
        async with self._lock:
            if self._dict.get(chat_id, None):
                return True
        return False

    async def take(self, chat_id):
        async with self._lock:
            if await self.in_conversation(chat_id):
                return self._dict.get(chat_id, None)

    async def take_yield(self, chat_id: int, limit: int = 6):
        idx: int = 0
        async with self._lock:
            get = self._dict.get(chat_id, None)
            if get is None:
                return
        while True:
            if idx >= limit:
                return
            idx += 1
            try:
                yield await get.__anext__()
            except StopAsyncIteration:
                await self.dismiss(chat_id)
                return
            except Exception as _:
                logging.exception(f"unhandled error for {chat_id}")
                await self.dismiss(chat_id)
                raise

    # async def do_signal(self, chat_id):
    #     async with self._lock:
    #         self._cp[chat_id] = True
