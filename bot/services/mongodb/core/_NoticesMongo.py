from bot.services.mongodb.classes import MFile
from bot.services.mongodb.core._MongoSession import _MongoSession


class _NoticesMongo(_MongoSession):

    async def notice_get_last_file_info(self):
        async for i in self.notices.find({}):
            return MFile(**i)

    async def notice_upload_file_info(self, date: str, file_id: str):
        return await self.notices.insert_one({'date': date, 'file_id': file_id})
