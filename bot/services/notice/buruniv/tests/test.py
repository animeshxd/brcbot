import logging
import unittest

from bot.services.notice.buruniv import NoticeType, UGUniversityNoticeClient

log = logging.getLogger(__name__)

class TestUGUniversityNoticeClient(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.client: UGUniversityNoticeClient= await UGUniversityNoticeClient().init()

    async def asyncTearDown(self) -> None:
        await self.client.close()

    async def test_fetch(self):
        result = await self.client.fetch(NoticeType.Examination)
        log.debug(result)
        self.assertIsNotNone(result)  

    async def test_iter_notices(self):
        async for i in self.client.iter_notices(type=NoticeType.Examination):
            log.debug(i)

        async for i in self.client.iter_notices(type=NoticeType.Examination, search="BCA"):
            log.debug(i)


if __name__ == '__main__':
    unittest.main()
