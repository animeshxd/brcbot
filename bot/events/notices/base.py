import typing

from pyrogram import Client
from pyrogram.types import ReplyKeyboardRemove, Message, InlineKeyboardButton, InlineKeyboardMarkup

import bot.events.buttons as b
from bot import db
from bot import notice, conv


def __parse(d: dict):
    date = d.get('dop', '')
    subject = d.get('subject', ' ')
    file = d.get('filename', '')
    button = None
    if file:
        file = f'https://burdwanrajcollege.ac.in/docs/notices/{file}'
        button = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text='Download PDF', url=file)]
            ]
        )
    text = f"""
Date: {date}
**{subject}**
Please download the file for details
    """.strip()

    return text, button


async def base(_c: Client, message: Message, text: str, search: str = '', limit_page: int = 0,
               x: typing.AsyncGenerator = None):
    if x is None:
        x = notice.iter_notices(search=search, limit_page=limit_page)
    await conv.put(message.chat.id, x)
    flag: bool = True
    m = await _c.send_message(message.chat.id, '...', reply_markup=ReplyKeyboardRemove())
    async for i in conv.take_yield(message.chat.id):
        if flag:
            await m.delete()
            await db(_c.send_message(message.chat.id, text))
            flag = False
        t, _ = __parse(i)
        await db(_c.send_message(message.chat.id, t, reply_markup=_))
    if flag:
        await m.delete()
        await db(_c.send_message(message.chat.id, 'No Notices were published', reply_markup=b.notice_buttons))
        return
    if await conv.in_conversation(message.chat.id):
        await db.one(_c.send_message(message.chat.id, '...', reply_markup=b.next_button))
    else:
        await db(_c.send_message(message.chat.id, '_', reply_markup=b.notice_buttons))
        # await db(_c.send_message(message.chat.id, 'Notices', reply_markup=b.notice_buttons))
