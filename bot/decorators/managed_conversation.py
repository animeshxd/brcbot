import functools

from pyrogram import Client
from pyrogram.types import Message, CallbackQuery

from bot.services.cache import Cache
from bot.services.conversation import Conversation


def managed_conversation(cache: Cache, conv: Conversation):

    def decorator(func):
        @functools.wraps(func)
        async def run(_c: Client, _m, *args, **kwargs):

            if isinstance(_m, CallbackQuery):
                chat_id = _m.from_user.id
            elif isinstance(_m, Message):
                chat_id = _m.from_user.id
            else:
                return
            if await conv.in_conversation(chat_id):
                await conv.dismiss(chat_id)
            m = await cache.take_1(chat_id)
            if m:
                await m.delete()
            return await func(_c, _m, *args, **kwargs)
        return run
    return decorator
