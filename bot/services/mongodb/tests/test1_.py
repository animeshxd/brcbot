from bot.services.mongodb import MongoSession
from config import MONGO_SRV


async def test():
    session = MongoSession(MONGO_SRV)
    result = await session.user_update(124)
    print(result)
    result = await session.user_find(124)
    print(result)

    async for i in session.user_iter(True, False):
        print(i)
    await session.db.notices.drop()
    await session.db.create_collection('notices', capped=True, size=100, max=1)
    # await session.notices.update_one({'_id': 1}, {"$set": dict(date='10-01-2003', file_id='Notice_76066555555244444.pdf')}, upsert=True)
    # await session.notices.update_one({'_id': 2}, {"$set": dict(date='10-01-2003', file_id='Notice_760665555552444433334.pdf')}, upsert=True)
    # await session.notices.update_one({'_id': 3}, {"$set": dict(date='10-01-2003', file_id='Notice_76066555555244443333dgfjirti.pdf')}, upsert=True)
    # await session.upload_file_info(date='10-01-2003', file_id='Notice_76066555555244444.pdf')
    # result = await session.get_last_file_info()
    # print(result)


if __name__ == '__main__':
    import asyncio
    asyncio.new_event_loop().run_until_complete(test())
