from datetime import datetime
from bot.services.mongodb.classes import MFile
from bot.services.mongodb.core._MongoSession import _MongoSession
from pymongo.results import InsertOneResult
from typing import Type

from bot.services.notice.interface import NoticeClient, NoticeType
from bot.services.notice.brc import CollegeNoticeClient


class _NoticesMongo(_MongoSession):
    
    async def notice_get_last_file_info(self, 
                                        client_type: Type[NoticeClient] | NoticeClient,
                                        notice_type: NoticeType | None = None
                                        ):
        db = self.db[f"{client_type.TAG}_{notice_type.value if notice_type else ''}"]
        async for i in db.find({}):
            return MFile(**i)


    async def notice_upload_file_info(self, date: datetime | None, 
                                      file_id: str, 
                                      client_type: Type[NoticeClient] | NoticeClient,
                                      notice_type: NoticeType | None = None
                                      ) -> InsertOneResult:
        assert date or file_id, "date and file_id are both None"
        db = self.db[f"{client_type.TAG}_{notice_type.value if notice_type else ''}"]
        data = {k:v for k,v in {'date': date, 'file_id': file_id}.items() if v is not None}
        return await db.update_one({'_id': 1},{'$set': data}, upsert=True)

