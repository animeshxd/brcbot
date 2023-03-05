import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot import destroy, init

from bot.mongo import mongo
from bot.services.scheduler import scheduler
from pyromongo import MongoStorage


if __name__ == '__main__':
    from bot import client, college_notice_client
    import bot.events.home
    import bot.events.menu
    import bot.events.settings
    import bot.events.notices
    import bot.events.about

    client.storage = MongoStorage(mongo.db)
    sched = AsyncIOScheduler()
    sched.add_job(scheduler, 'interval', hours=5, seconds=10, kwargs=dict(client=client, mongo=mongo, notices=college_notice_client, _scheduler=sched))
    sched.start()
    try:
        client.run(init())
        client.run()
    finally:
        asyncio.new_event_loop().run_until_complete(destroy())
