from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClient, AsyncIOMotorDatabase


class _MongoSession(object):
    mongo: AsyncIOMotorClient
    notices: AsyncIOMotorCollection
    users: AsyncIOMotorCollection

    def __init__(self, src: str, testing: bool = False) -> None:
        self.testing = testing
        self.mongo = AsyncIOMotorClient(src)
        db: AsyncIOMotorDatabase = self.mongo['test_brc'] if testing else self.mongo['brc']
        self.db = db
        self.notices = db['notices']
        self.users = db['users']

    async def init(self):
        collection_name = "notices"
        if collection_name not in await self.db.list_collection_names():
            await self.db.create_collection(collection_name, capped=True, size=100, max=1)

    async def drop_test_database(self):
        if self.testing:
            await self.mongo.drop_database("test_brc")
