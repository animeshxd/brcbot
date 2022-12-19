
import config
from bot.const import profiles


def development_only(func):
    async def run(client, event, *args, **kwargs):
        if config.PROFILE == profiles.DEVELOPMENT:
            return await func(client, event, *args, **kwargs)

    return run
