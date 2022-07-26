import functools

from pyrogram import Client
from pyrogram.types import Message

from bot.services.cache import Cache


def delete_from_sender(cache: Cache, later=False):
    def decorator(func):
        @functools.wraps(func)
        async def runner(client: Client, message: Message, *args, **kwargs):
            if later:
                await cache.safe_insert(message)
            else:
                await message.delete()
            return await func(client, message, *args, **kwargs)
        return runner
    return decorator
