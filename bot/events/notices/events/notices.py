import datetime

from pyrogram import Client, filters
from pyrogram.types import Message, ForceReply

from bot import client, db, college_notice_client
from bot.decorators.managed_event import managed_event
from bot.decorators.unimplemented import unimplemented
from bot.events import buttons as b
from bot.events.notices.base.utils import for_week_only
from bot.events.notices.events import handle

G = 4


@client.on_message(filters=filters.private & filters.regex('Notices|𝖡𝖺𝖼𝗄') | filters.command('notices'), group=G)
@managed_event
async def notices(_c: Client, message: Message, *args, **kwargs):
    await db(_c.send_message(message.chat.id, "Notices", reply_markup=b.notice_buttons))


@client.on_message(filters=filters.private & filters.regex('Search'), group=G)
@managed_event
async def search(_c: Client, message: Message, *args, **kwargs):
    await db(message.reply('Search', reply_markup=ForceReply(placeholder='Search...')))


@client.on_message(filters=filters.private & filters.regex('Today'), group=G)
@managed_event
async def today(_c: Client, message: Message, *args, **kwargs):
    now = datetime.datetime.now()
    await handle(_c, message, f'Today - {now.strftime("%d %B, %Y")}', search=now.strftime('%Y-%m-%d'))


@client.on_message(filters=filters.private & filters.regex('Latest'), group=G)
@managed_event
async def latest(_c: Client, message: Message, *args, **kwargs):
    await handle(_c, message, 'Latest', limit_page=1)


@client.on_message(filters=filters.private & filters.regex('Yesterday'), group=G)
@managed_event
async def yesterday(_c: Client, message: Message, *args, **kwargs):
    date = datetime.datetime.now() - datetime.timedelta(days=1)
    await handle(_c, message, f'Yesterday - {date.strftime("%d %B, %Y")}', search=date.strftime('%Y-%m-%d'))


@client.on_message(filters=filters.private & filters.regex('Last 7 Days'), group=G)
@managed_event
async def week(_c: Client, message: Message, *args, **kwargs):
    now = datetime.datetime.now()
    last = now - datetime.timedelta(weeks=1)
    await handle(_c, message, f'{now.strftime("%d %B, %Y")} - {last.strftime("%d %B, %Y")}',
                 async_generator=for_week_only(college_notice_client, last))


@client.on_message(filters=filters.private & filters.regex('This Month'), group=G)
@managed_event
async def month(_c: Client, message: Message, *args, **kwargs):
    now = datetime.datetime.now()
    await handle(_c, message, f'This Month - {now.strftime("%B, %Y")}', search=now.strftime('%Y-%m'))


@client.on_message(filters=filters.private & filters.regex('By Date'), group=G)
@managed_event
@unimplemented(db)
async def search_by_date(_c: Client, message: Message, *args, **kwargs):
    #LAST = "2022-03-02"
    pass


@client.on_message(filters=filters.private & filters.regex(r'\d{4}-\d{2}-\d{2}'), group=G)
@managed_event
async def on_date(_c: Client, message: Message, *args, **kwargs):
    await handle(_c, message, message.text, search=message.text)
