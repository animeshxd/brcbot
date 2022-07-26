import asyncio
import functools
import logging
import traceback

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram.client import Client

from bot.services.brc import Notices
from bot.services.mongodb import MongoSession

ADMIN = '@dotdml'

# async def if_failed_scheduler(*args, **kwargs):
#     await asyncio.sleep(5000)
#     await scheduler(*args, **kwargs)


def if_failed(func):
    @functools.wraps(func)
    async def run(client: Client, *args, **kwargs):
        try:
            await func(client, *args, **kwargs)
        except RuntimeError as e:
            await client.send_message(ADMIN, str(e))
            # await if_failed_scheduler(client, *args, **kwargs)
        except Exception:
            await client.send_message(ADMIN, f'```{traceback.format_exc()}```')
            # await if_failed_scheduler(client, *args, *kwargs)

    return run


@if_failed
async def scheduler(client: Client, mongo: MongoSession, notices: Notices, _scheduler: AsyncIOScheduler = None):
    last = await mongo.notice_get_last_file_info()
    subscribers = mongo.user_iter()
    send_to = []
    notices_ = ""
    try:
        async for index, i in notices.iter_from(date=last.date, file_id=last.file_id):
            # text, button = parse(i)
            # await client.send_message()
            date = i.get('dop', '')
            subject = i.get('subject', ' ')
            file = i.get('filename', '')
            if file:
                file = f'https://burdwanrajcollege.ac.in/docs/notices/{file}'
            notices_ = (
                           f"{index}.\n"
                           f"Date: {date}\n"
                           f"**{subject}**\n"
                           f"[[Download PDF]({file})]\n"
                           f"________________________________\n"
                       ) + notices_
            await mongo.notice_upload_file_info(date=i['don'], file_id=i['filename'])
        if not notices_:
            logging.info('empty notices')
            return
        await asyncio.sleep(10)
        idx: int = 0
        async for i in subscribers:
            idx += 1
            if idx % 5 == 0:
                await asyncio.sleep(6)
            try:
                await client.send_message(i.id, notices_, disable_web_page_preview=True)
            except Exception as e:
                logging.error(traceback.format_exc())
                continue
            send_to.append(i.id)

        # print(notices_)
    except Exception as _:
        if send_to:
            await mongo.users.update({'_id': {'$in': send_to}}, {'$set': {'notified': True}}, multi=True)
        raise _
