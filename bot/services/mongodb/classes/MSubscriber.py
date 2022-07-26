from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorCollection


@dataclass
class MSubscriber:
    _coll: AsyncIOMotorCollection
    _id: int
    id: int = None
    stopped: bool = True
    subscribed: bool = False
    notified: bool = True

    async def set_notified(self):
        await self._coll.update_one({'_id': self.id}, {'$set': {'notified': True}})

