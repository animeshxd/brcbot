import logging
import unittest
from pyrogram import Client
import config as V
from bot import CollegeNoticeClient
from bot.services.mongodb import MongoSession
from bot.services.scheduler import notice_scheduler


log = logging.getLogger(__name__)

class TestScheduler(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.client = Client("")
        self.client.send_message = self.mock_send_message
        self.notices = await CollegeNoticeClient().init()
        self.mongo = MongoSession(V.MONGO_SRV, testing=True)
        await self.mongo.user_add_bulk(range(5), subscribed=True)
        notices = await self.notices.fetch()
        await self.mongo.notice_upload_file_info(date=notices['data'][2]['don'], file_id=notices['data'][2]['filename'])
    
    @staticmethod
    async def mock_send_message(*args, **kwargs):
        # log.debug(args, kwargs)
        ...

    async def asyncTearDown(self) -> None:
        await self.notices.close()
        await self.mongo.drop_test_database()

    async def test_scheduler(self):
        await notice_scheduler(self.client, self.mongo, self.notices)

        

if __name__ == '__main__':
    unittest.main()
