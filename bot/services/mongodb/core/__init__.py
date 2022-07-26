from bot.services.mongodb.core._NoticesMongo import _NoticesMongo
from bot.services.mongodb.core._UsersMongo import _UsersMongo


class MongoSession(_NoticesMongo, _UsersMongo):
    pass
