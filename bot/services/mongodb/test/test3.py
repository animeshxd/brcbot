from bot.services.mongodb.core import _NoticesMongo
from config import MONGO_SRV


async def test3():
    session = _NoticesMongo(MONGO_SRV)
    await session.db.notices.drop()
    await session.db.create_collection('notices', capped=True, size=100, max=1)
    await session.notice_upload_file_info('2022-07-14', 'Notice_14072022_88.pdf')
    file = await session.notice_get_last_file_info()
    print(file)


if __name__ == '__main__':
    import asyncio
    asyncio.new_event_loop().run_until_complete(test3())