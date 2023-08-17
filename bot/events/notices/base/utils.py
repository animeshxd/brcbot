import datetime
import typing

from pyrogram import Client
from pyrogram.types import ReplyKeyboardRemove, Message, InlineKeyboardButton, InlineKeyboardMarkup

import bot.events.buttons as b
from bot.services.notice.brc.client import CollegeNoticeClient, get_dict_to_notice
from bot.services.notice.data import Notice
from bot.services.notice.interface import NoticeClient
from bot.services.cache import Cache
from bot.services.conversation import Conversation


def parse_notice(d: Notice):
    date = d.extra
    subject = d.subject
    file = d.fileurl
    button = None
    if file:
        button = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text='Download PDF', url=file)]
            ]
        )
    text = f"""
Date: {date}
**{subject}**
Please download the file for details[.]({file if file else ''})
    """.strip()

    return text, button


async def handle(
        _c: Client,
        message: Message,
        text: str,
        notice: NoticeClient,
        cache: Cache,
        conv: Conversation,
        search: str = '', 
        limit_page: int = 0,
        async_generator: typing.AsyncGenerator[Notice, None] | None = None):
    if async_generator is None:
        async_generator = notice.iter_notices(search=search, limit_page=limit_page)
    await conv.put(message.chat.id, async_generator)
    flag: bool = True
    m = await _c.send_message(message.chat.id, '...', reply_markup=ReplyKeyboardRemove())
    async for i in conv.take_yield(message.chat.id):
        if flag:
            await m.delete()
            await cache(_c.send_message(message.chat.id, text))
            flag = False
        t, _ = parse_notice(i)
        await cache(_c.send_message(message.chat.id, t, reply_markup=_, disable_web_page_preview=False))
    if flag:
        await m.delete()
        await cache(_c.send_message(message.chat.id, 'No Notices were published', reply_markup=b.notice_buttons))
        return
    if await conv.in_conversation(message.chat.id):
        await cache.one(_c.send_message(message.chat.id, '...', reply_markup=b.next_button))
    else:
        await cache(_c.send_message(message.chat.id, '_', reply_markup=b.notice_buttons))
        # await db(_c.send_message(message.chat.id, 'Notices', reply_markup=b.notice_buttons))



async def for_week_only(notices: CollegeNoticeClient, last: datetime.datetime = datetime.datetime.now() - datetime.timedelta(weeks=1)):
    # print(last_week)
    _data = await notices.fetch()
    data = _data['data']
    if not data:
        return
    point = None
    for index, i in zip(range(len(data), -1, -1), reversed(data)):

        _ = datetime.datetime.strptime(i['don'], '%Y-%m-%d')
        # print(index, _ > last_week,  i)
        if _ < last:
            continue
        else:
            point = index
            break
    if point is None:  # sus
        return

    for i in data[:point]:
        yield get_dict_to_notice(i)


async def test():
    async with CollegeNoticeClient() as n:
        # await for_week_only(n)
        async for i in for_week_only(n):
            print(i)


if __name__ == '__main__':
    import asyncio

    asyncio.new_event_loop().run_until_complete(test())
