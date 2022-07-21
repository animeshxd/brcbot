import asyncio
import logging

from bot import Notices, Conversation


async def test():
    async with Notices() as notices:
        # data = await notices.fetch(page=8)
        # print(data)

        x = notices.iter_notices()
        # print(await x.__anext__())
        # print(await x.__anext__())
        # print(await x.__anext__())
        # async for i in x:
        #     print(i)
        # await x.aclose()
        # async for i in x:
        #     print(i)

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
    asyncio.new_event_loop().run_until_complete(test())
