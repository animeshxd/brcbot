from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClient, AsyncIOMotorDatabase


class _MongoSession(object):
    mongo: AsyncIOMotorClient
    notices: AsyncIOMotorCollection
    users: AsyncIOMotorCollection

    def __init__(self, src: str):
        self.mongo = AsyncIOMotorClient(src)
        db: AsyncIOMotorDatabase = self.mongo['brc']
        self.db = db
        self.notices = db['notices']
        self.users = db['users']
