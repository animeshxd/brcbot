import asyncio.exceptions
import functools
import logging

from aiohttp import ServerDisconnectedError
from pyrogram.client import Client
from pyrogram.types import Message

from bot.services.cache import Cache
from bot.events.buttons import home_buttons


def suppress_error(cache: Cache):
    def decorator(func):
        @functools.wraps(func)
        async def run(_c: Client, _m: Message, *args, **kwargs):
            try:
                return await func(_c, _m, *args, **kwargs)
            except RuntimeError:
                await cache(_m.reply('RuntimeError: Something went wrong', reply_markup=home_buttons))
            except asyncio.exceptions.TimeoutError:
                await cache(_m.reply("TimeoutError: time limit exceed, try again later", reply_markup=home_buttons))
            except ServerDisconnectedError:
                await cache(_m.reply("ServerDisconnectedError: we got disconnected from server, try again later",
                                     reply_markup=home_buttons))
            except Exception as e:
                logging.exception(f"unhandled error for user {_m.chat.id}")
                await cache(_m.reply("UnexpectedError: failed to handle this", reply_markup=home_buttons))

        return run
    return decorator
