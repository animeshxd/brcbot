import logging
import unittest

from bot.services.notice.brc import CollegeNoticeClient

log = logging.getLogger(__name__)

class TestCollegeNoticeClient(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.notices = CollegeNoticeClient()
        await self.notices.init()

    async def asyncTearDown(self) -> None:
        await self.notices.close()

    async def test_fetch(self):
        result = await self.notices.fetch()
        self.assertGreater(len(result), 0, "got empty result")
        self.assertIn('data', result, "result['data']  not found")
        items = result['data']
        log.info(items)
        self.assertGreater(len(items), 0, "got empty result['data']")
        with self.subTest(data=items[0]):
            self.assertIn('don', items[0], "result['data'][0]['don'] not found")
        with self.subTest(data=items[0]):
            self.assertIn('dop', items[0], "result['data'][0]['dop'] not found")
        with self.subTest(data=items[0]):
            self.assertIn('subject', items[0], "result['data'][0]['subject'] not found")
        with self.subTest(data=items[0]):
            self.assertIn('filename', items[0], "result['data'][0]['filename'] not found")

    async def test_iter_notices(self):
        async with CollegeNoticeClient() as notices:
            self.assertGreater(len([i async for i in notices.iter_notices()]), 0, "empty notices.iter_notices()")

    async def test_iter_after(self):
        async with CollegeNoticeClient() as notices:
            self.assertGreater(len([i async for i in notices.iter_after(file_id="Notice_07022023_159.pdf")]), 0, "empty notices.iter_notices()")


if __name__ == '__main__':
    unittest.main()
