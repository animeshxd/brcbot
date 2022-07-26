from pyrogram import filters, Client
from pyrogram.types import Message

from bot import client
from bot.decorators.managed_event import managed_event
from bot.decorators.on_reply_message import on_reply_message
from bot.events.notices.events import base


@client.on_message(filters=filters.private & filters.reply, group=2)
@managed_event
@on_reply_message('Search')
async def settings(_c: Client, message: Message, *args, **kwargs):
    await base(_c, message, f'Results for {message.text}', search=message.text)

