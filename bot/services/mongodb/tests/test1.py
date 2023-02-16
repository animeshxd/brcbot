import unittest

from pymongo.results import UpdateResult

from bot.services.mongodb import MongoSession
from config import MONGO_SRV


class TestMongoSession(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.session = MongoSession(MONGO_SRV, testing=True)
        await self.session.init()

    async def asyncTearDown(self) -> None:
        print("dropped")
        await self.session.drop_test_database()

    async def test_user_methods(self):
        for i in range(100):
            await self.session.user_update(i)

        with self.subTest():
            result = await self.session.user_find(99)
            print(result)
            self.assertIsNotNone(result, "user_update failed")

        with self.subTest():
            total = len([i async for i in self.session.user_iter(stopped=True, subscribed=False)])
            print(total)
            self.assertGreater(total, 0, "user_update failed")

        with self.subTest():
            total = await self.session.users.count_documents({})
            self.assertGreater(total, 0, "user_update failed")



if __name__ == '__main__':
    TestMongoSession().run()
