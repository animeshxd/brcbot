import functools

from pyrogram import Client
from pyrogram.types import Message


def on_reply_message(text: str):
    def decorator(func):
        @functools.wraps(func)
        async def run(client: Client, message: Message, *args, **kwargs):
            reply: Message = message.reply_to_message
            # print(reply)
            if text == reply.text:
                await func(client, message, *args, **kwargs)
        return run
    return decorator
