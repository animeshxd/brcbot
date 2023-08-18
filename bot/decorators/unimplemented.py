import functools

from bot.events.buttons import notice_buttons
from bot.services.cache import Cache


def unimplimented(cache: Cache):
    def decorator(func):
        @functools.wraps(func)
        async def run(_c, _m, *_a, **_k):
            await cache(_m.reply("This feature is not implemented yet.", reply_markup=notice_buttons))
        return run
    return decorator
