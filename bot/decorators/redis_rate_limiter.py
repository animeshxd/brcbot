import functools
import logging
from datetime import timedelta

from pyrogram.client import Client
from pyrogram.types import Message
from bot.redisc import rd

LIMIT = 9
EXPIRE = timedelta(seconds=30)

log = logging.getLogger(__name__)


def ratelimited(cache, limit=LIMIT, expires=EXPIRE, ):
    def decorator(func):
        @functools.wraps(func)
        async def run(_c: Client, _m: Message, *args, **kwargs):
            r = await rd.incr(_m.chat.id)
            if r == 1:
                await rd.expire(_m.chat.id, time=expires)
            if r > limit:
                ttl = await rd.ttl(_m.chat.id)
                log.debug(f"request times {r} exceed for user {_m.chat.id}")
                await cache(_m.reply(f"Too many requests within {expires.seconds} seconds, wait {ttl} seconds"))
                return
            log.debug(f"request times {r} for user {_m.chat.id}")
            await func(_c, _m, *args, **kwargs)
        return run
    return decorator


