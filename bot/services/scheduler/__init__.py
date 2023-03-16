import asyncio
import functools
import logging
import traceback
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram.client import Client

from bot.services.mongodb import MongoSession
from bot.services.mongodb.classes import MFile
from bot.services.notice.data import Notice
from bot.services.notice.interface import NoticeType, NoticeClient

ADMIN = 'dotdml'

# async def if_failed_scheduler(*args, **kwargs):
#     await asyncio.sleep(5000)
#     await scheduler(*args, **kwargs)

log = logging.getLogger(__name__)
client: Client

def if_failed(func):
    @functools.wraps(func)
    async def run(client: Client, *args, **kwargs):
        try:
            await func(client, *args, **kwargs)
        except RuntimeError as e:
            await client.send_message(ADMIN, str(e))
            # await if_failed_scheduler(client, *args, **kwargs)
        except Exception:
            log.exception("error")
            await client.send_message(ADMIN, f'```{traceback.format_exc()}```')
            # await if_failed_scheduler(client, *args, *kwargs)

    return run


@if_failed
async def notice_scheduler(client: Client,
                    mongo: MongoSession,
                    notices: NoticeClient, 
                    _type: NoticeType | None,
                    _scheduler: Optional[AsyncIOScheduler] = None,
                    ):
    last = await mongo.notice_get_last_file_info(notices, _type)
    subscribers = mongo.user_iter(subscribed=True)
    send_to = []
    notices_ = ""
    if not last:
        i: Notice
        async for i in notices.iter_notices(type=_type): # type: ignore
            await mongo.notice_upload_file_info(i.date, i.filename, notices, _type)
            last = MFile(_id='', id='', date=i.date, file_id=i.filename)
            break
    try:
        async for index, i in notices.iter_after(file_id=last.file_id, date=last.date, type=_type):  # type: ignore
            date = i.extra
            subject = i.subject
            file = i.fileurl
            notices_ = (
                           f"{index}.\n"
                           f"Date: {date}\n"
                           f"**{subject}**\n"
                           f"[[Download PDF]({file})]\n"
                           f"________________________________\n"
                       ) + notices_
            await mongo.notice_upload_file_info(i.date, i.filename, notices, _type)
        if not notices_:
            log.info(f'empty notices with {type(notices)} : {_type.value if _type else ""}')
            return
        notices_+= f'#{notices.TAG} #{_type.value if _type else ""}'
        idx: int = 0
        
        async for subscriber in subscribers:
            idx += 1
            if idx % 5 == 0:
                await asyncio.sleep(6)
            try:
                await client.send_message(subscriber.id, notices_, disable_web_page_preview=True)
            except Exception as e:
                log.exception(f"error occurs for user {subscriber.id}")
                continue
            send_to.append(subscriber.id)

        # print(notices_)
    except Exception as _:
        if send_to:
            await mongo.user_update_many(send_to, notified=True)
        raise
    if not send_to:
        log.debug("No one is subscribed")
