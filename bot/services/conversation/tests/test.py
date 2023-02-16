import unittest

from ...conversation import Conversation
from ...notice.brc import CollegeNoticeClient


async def test2():
    async with CollegeNoticeClient as notices:
        x = await notices.iter_notices()
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


class TestConversation(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.conv = Conversation()
        self.client = CollegeNoticeClient()
        await self.client.init()

    async def asyncTearDown(self) -> None:
        await self.client.close()

    async def test_take_yield(self):
        x = self.client.iter_notices()

        await self.conv.put(1, x)
        self.assertGreater(len([i async for i in self.conv.take_yield(1)]), 0, "Conversation.take_yield(1) empty")


if __name__ == '__main__':
    TestConversation().run()
