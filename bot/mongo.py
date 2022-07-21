from config import MONGO_SRV

from bot.services.mongodb import MongoSession

mongo = MongoSession(MONGO_SRV)
