from datetime import datetime
import logging
import unittest

from pymongo.results import UpdateResult

from bot.services.mongodb import MongoSession
from bot.services.notice.brc.client import CollegeNoticeClient
from config import MONGO_SRV

log = logging.getLogger(__name__)

class TestMongoSession(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.session = MongoSession(MONGO_SRV, testing=True)

    async def asyncTearDown(self) -> None:
        print("dropped")
        await self.session.drop_test_database()

    async def test_user_methods(self):
        for i in range(100):
            await self.session.user_add(i)

        with self.subTest("session.user_find"):
            result = await self.session.user_find(99)
            self.assertIsNotNone(result, "session.user_find(99) failed")

        with self.subTest("session.user_iter"):
            total = len([i async for i in self.session.user_iter(stopped=False, subscribed=False)])
            self.assertGreater(total, 0, "session.user_iter() failed")

        with self.subTest("users.count_documents"):
            total = await self.session.users.count_documents({})
            self.assertGreater(total, 0, "user_update failed")

    async def test_notice_methods(self):
        date = datetime(day=7, month=2, year=2023)
        file_id = 'Notice_07022023_160.pdf'
        await self.session.notice_upload_file_info(date, file_id, CollegeNoticeClient)
        result = await self.session.notice_get_last_file_info(CollegeNoticeClient)
        log.info(result)
        self.assertEqual(date, result.date)
        self.assertEqual(file_id, result.file_id)


if __name__ == '__main__':
    unittest.main()
