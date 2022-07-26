import functools

from bot.decorators.delete_from_sender import delete_from_sender
from bot.decorators.managed_conversation import managed_conversation
from bot.decorators.suppress_error import suppress_error
from bot import db, conv


def managed_event(func):
    @functools.wraps(func)
    @delete_from_sender(db, True)
    @managed_conversation(db, conv)
    @suppress_error(db)
    async def run(client, event, *args, **kwargs):
        return await func(client, event, *args, **kwargs)

    return run
