import functools

from bot import db


def unimplimented(func):
    @functools.wraps(func)
    async def run(_c, _m, *_a, **_k):
        await db(_m.reply("This feature is not implimented yet."))
    return run
