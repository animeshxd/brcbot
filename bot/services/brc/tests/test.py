import asyncio
import logging

from bot.services.conversation import Conversation
from bot.services.brc import Notices


async def test():
    async with Notices() as notices:
        # data = await notices.fetch(page=8)
        # print(data)

        # assert [i async for i in notices.iter_notices()], "empty notices.iter_notices()"

        assert [i async for i in notices.iter_from(file_id="Notice_11102022_111.pdf")], "empty"


async def test2():
    async with Notices() as notices:
        x = notices.iter_notices()
        print(await x.__anext__())
        print(await x.__anext__())
        print(await x.__anext__())
        async for i in x:
            print(i)
        await x.aclose()
        async for i in x:
            print(i)
        c = Conversation()
        await c.put(1, x)
        # await c.put(1, x)
        async for i in c.take_yield(1):
            print(i)
        # print('_')
        async for i in c.take_yield(1):
            print(i)
        print('end')
            # pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.new_event_loop().run_until_complete(test2())
