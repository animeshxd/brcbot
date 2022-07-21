import functools

from bot.decorators.delete_from_sender import delete_from_sender
from bot.decorators.managed_conversation import managed_conversation
from bot.decorators.suppress_error import suppress_error


def managed_event(func):
    @functools.wraps(func)
    @delete_from_sender(True)
    @managed_conversation
    @suppress_error
    async def run(client, event, *args, **kwargs):
        return await func(client, event, *args, **kwargs)
    return run