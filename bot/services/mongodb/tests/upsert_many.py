from bot.services.mongodb.core import _NoticesMongo
from config import MONGO_SRV
from pymongo import UpdateOne

async def test4():
    session = _NoticesMongo(MONGO_SRV)
    await session.db.test.drop()
    print(await session.db.list_collections())
    coll = session.db.test
    await coll.insert_one({'_id': 1, 'type': 2})
    bulk = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    ]
    await coll.bulk_write(
        [
            UpdateOne({'_id': i[0]}, {'$set': {'type': i[1]}}, upsert=True) for i in bulk
        ]
    )

    async for i in coll.find({}):
        print(i)


if __name__ == '__main__':
    import asyncio
    asyncio.new_event_loop().run_until_complete(test4())