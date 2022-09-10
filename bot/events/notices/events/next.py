from pyrogram import filters, Client
from pyrogram.types import Message, ReplyKeyboardRemove

from bot import client, conv, db
from bot.decorators.delete_from_sender import delete_from_sender
from bot.decorators.radis_rate_limiter import ratelimited
from bot.decorators.suppress_error import suppress_error
from bot.events import buttons
from bot.events.notices import base


@client.on_message(filters=filters.private & filters.regex('Next') | filters.command('next'), group=4)
@delete_from_sender(db, True)
@suppress_error(db)
@ratelimited()
async def next_(_c: Client, _m: Message, *args, **kwargs):
    await _m.delete()
    clr = await db.take_1(_m.chat.id)
    if clr:
        await clr.delete()
    m = await _c.send_message(_m.chat.id, '...', reply_markup=ReplyKeyboardRemove())
    await m.delete()
    if await conv.in_conversation(_m.chat.id):
        async for i in conv.take_yield(chat_id=_m.chat.id):
            text, button = base.parse(i)
            await db(_c.send_message(_m.chat.id, text, reply_markup=button))
        incnv = await conv.in_conversation(_m.chat.id)
        if incnv:
            await db.one(_c.send_message(_m.chat.id, "...", reply_markup=buttons.next_button))
            return
        await db.one(_c.send_message(_m.chat.id, '_', reply_markup=buttons.notice_buttons))
        return
    else:
        await db(_c.send_message(_m.chat.id, 'Notices', reply_markup=buttons.notice_buttons))
