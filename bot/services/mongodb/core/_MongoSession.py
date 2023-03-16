from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClient, AsyncIOMotorDatabase


class _MongoSession(object):
    mongo: AsyncIOMotorClient # type: ignore
    users: AsyncIOMotorCollection # type: ignore

    def __init__(self, src: str, testing: bool = False) -> None:
        self.testing = testing
        self.mongo = AsyncIOMotorClient(src)
        db: AsyncIOMotorDatabase = self.mongo['test_brc'] if testing else self.mongo['brc'] # type: ignore
        self.db = db
        self.users = db['users']


    async def drop_test_database(self):
        if self.testing:
            await self.mongo.drop_database("test_brc")
