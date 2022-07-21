import datetime

from pyrogram import Client, filters
from pyrogram.types import Message, ForceReply

from bot import client, db, notice
from bot.decorators.managed_event import managed_event
from bot.events import buttons as b
from bot.events.notices.base import base
from bot.events.notices.helpers import for_week_only
from bot.decorators.unimplimented import unimplimented


@client.on_message(filters=filters.private & filters.regex('Notices|𝖡𝖺𝖼𝗄') | filters.command('notices'), group=4)
@managed_event
async def notices(_c: Client, message: Message, *args, **kwargs):
    await db(_c.send_message(message.chat.id, "Notices", reply_markup=b.notice_buttons))


@client.on_message(filters=filters.private & filters.regex('Search'), group=4)
@managed_event
async def search(_c: Client, message: Message, *args, **kwargs):
    await db(message.reply('Search', reply_markup=ForceReply(placeholder='Search...')))


@client.on_message(filters=filters.private & filters.regex('Today'), group=4)
@managed_event
async def today(_c: Client, message: Message, *args, **kwargs):
    now = datetime.datetime.now()
    await base(_c, message, f'Today - {now.strftime("%d %B, %Y")}', search=now.strftime('%Y-%m-%d'))


@client.on_message(filters=filters.private & filters.regex('Latest'), group=4)
@managed_event
async def latest(_c: Client, message: Message, *args, **kwargs):
    await base(_c, message, 'Latest', limit_page=1)


@client.on_message(filters=filters.private & filters.regex('Yesterday'), group=4)
@managed_event
async def yesterday(_c: Client, message: Message, *args, **kwargs):
    date = datetime.datetime.now() - datetime.timedelta(days=1)
    await base(_c, message, f'Yesterday - {date.strftime("%d %B, %Y")}', search=date.strftime('%Y-%m-%d'))


@client.on_message(filters=filters.private & filters.regex('Last 7 Days'), group=4)
@managed_event
async def week(_c: Client, message: Message, *args, **kwargs):
    now = datetime.datetime.now()
    last = now - datetime.timedelta(weeks=1)
    await base(_c, message, f'{now.strftime("%d %B, %Y")} - {last.strftime("%d %B, %Y")}',
               x=for_week_only(notice, last))


@client.on_message(filters=filters.private & filters.regex('This Month'), group=4)
@managed_event
async def month(_c: Client, message: Message, *args, **kwargs):
    now = datetime.datetime.now()
    await base(_c, message, f'This Month - {now.strftime("%B, %Y")}', search=now.strftime('%Y-%m'))


@client.on_message(filters=filters.private & filters.regex('by Date'), group=4)
@managed_event
@unimplimented
async def search_by_date(_c: Client, message: Message, *args, **kwargs):
    pass

# TODO: Implement Conversation with Produces Consumer


