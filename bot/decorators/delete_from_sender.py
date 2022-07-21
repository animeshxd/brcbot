import functools

from pyrogram import Client
from pyrogram.types import Message

from bot import db


def delete_from_sender(later=False):
    def decorator(func):
        @functools.wraps(func)
        async def runner(client: Client, message: Message, *args, **kwargs):
            if later:
                await db.safe_insert(message)
            else:
                await message.delete()
            return await func(client, message, *args, **kwargs)
        return runner
    return decorator
