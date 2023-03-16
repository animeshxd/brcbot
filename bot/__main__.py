import asyncio
from typing import Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot import destroy, init

from bot.mongo import mongo
from bot.services.scheduler import notice_scheduler
from bot.services.notice.buruniv import UGUniversityNoticeType
from pyromongo import MongoStorage


def start_scheduler(client, college_notice_client, university_notice_client):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(notice_scheduler, 'interval', hours=2, 
                  kwargs=dict(client=client, mongo=mongo, notices=college_notice_client, _scheduler=scheduler, _type=None))
    
    for _type in (UGUniversityNoticeType.Admission,
                  UGUniversityNoticeType.Examination,
                  UGUniversityNoticeType.Results
                ):
        scheduler.add_job(notice_scheduler, 'interval', hours=2, 
                      kwargs=dict(client=client, mongo=mongo, notices=university_notice_client, _scheduler=scheduler, _type=_type))
    scheduler.start()
    return scheduler

if __name__ == '__main__':
    from bot import client, college_notice_client, university_notice_client
    import bot.events.home
    import bot.events.menu
    import bot.events.settings
    import bot.events.notices
    import bot.events.about

    client.storage = MongoStorage(mongo.db) # type: ignore
    scheduler = start_scheduler(client, college_notice_client, university_notice_client)
    try:
        client.run(init())
        client.run()
    finally:
        scheduler.shutdown()
        asyncio.new_event_loop().run_until_complete(destroy())
