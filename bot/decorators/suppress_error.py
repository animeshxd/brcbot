import asyncio.exceptions
import functools
import logging
import traceback

from pyrogram import Client
from pyrogram.types import Message


def suppress_error(func):
    @functools.wraps(func)
    async def run(_c: Client, _m: Message, *args, **kwargs):
        try:
            return await func(_c, _m, *args, **kwargs)
        except RuntimeError:
            await _m.reply('RuntimeError: Something went wrong')
        except asyncio.exceptions.TimeoutError:
            await _m.reply("TimeoutError: time limit exceed, try again later")
        except Exception as e:
            logging.error(traceback.format_exc())
            await _m.reply("UnexpectedError: failed to handle this")

    return run
