import logging
import unittest

from bot.services.notice.buruniv import UGUniversityNoticeType, UGUniversityNoticeClient

log = logging.getLogger(__name__)


class TestUGUniversityNoticeClient(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.client: UGUniversityNoticeClient = await UGUniversityNoticeClient().init()

    async def asyncTearDown(self) -> None:
        await self.client.close()

    async def test_fetch(self):
        result = await self.client.fetch(UGUniversityNoticeType.Examination)
        log.debug(result)
        self.assertIsNotNone(result)

    async def test_iter_notices(self):
        async for i in self.client.iter_notices(type=UGUniversityNoticeType.Examination):
            log.debug(i)

        async for i in self.client.iter_notices(type=UGUniversityNoticeType.Examination, search="BCA"):
            log.debug(i)

    async def test_iter_notices_type_Examination(self):
        async for i in self.client.iter_notices(UGUniversityNoticeType.Examination):
            log.debug(i)

    async def test_iter_notices_type_Results(self):
        async for i in self.client.iter_notices(UGUniversityNoticeType.Results):
            log.debug(i)

    async def test_iter_notices_type_Admission(self):
        async for i in self.client.iter_notices(UGUniversityNoticeType.Admission):
            log.debug(i)

    async def test_iter_after(self):
        async for i in self.client.iter_after(type=UGUniversityNoticeType.Examination, file_id='20231043_CE.pdf'):
            log.debug(i)


if __name__ == '__main__':
    unittest.main()
