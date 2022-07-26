import functools


def on_raw_type(_type):
    def decorator(func):
        @functools.wraps(func)
        async def run(client, update, *args, **kwargs):
            if isinstance(update, _type):
                await func(client, update, *args, **kwargs)
        return run
    return decorator


