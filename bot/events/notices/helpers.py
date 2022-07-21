import datetime

from bot.services.brc import Notices


async def for_week_only(notices: Notices, last: datetime.datetime = datetime.datetime.now() - datetime.timedelta(weeks=1)):
    # print(last_week)
    _data = await notices.fetch()
    data = _data['data']
    if not data:
        return
    point = None
    for index, i in zip(range(len(data), -1, -1), reversed(data)):

        _ = datetime.datetime.strptime(i['don'], '%Y-%m-%d')
        # print(index, _ > last_week,  i)
        if _ < last:
            continue
        else:
            point = index
            break
    if point is None:  # sus
        return

    for i in data[:point]:
        yield i


async def test():
    async with Notices() as n:
        # await for_week_only(n)
        async for i in for_week_only(n):
            print(i)


if __name__ == '__main__':
    import asyncio

    asyncio.new_event_loop().run_until_complete(test())
