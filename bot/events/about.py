from pyrogram.client import Client
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from bot import client, db
from bot.decorators.managed_event import managed_event
from bot.events import buttons


@client.on_message(filters=filters.private & filters.regex('^About$') | filters.command('about'), group=4)
@managed_event
async def about(_c: Client, message: Message, *args, **kwargs):
    await db(_c.send_message(message.chat.id, 'About', reply_markup=buttons.about_button))


@client.on_message(filters=filters.private & filters.regex('About Bot') | filters.command('bot'), group=4)
@managed_event
async def about_bot(_c: Client, message: Message, *args, **kwargs):
    text = """
    **About Bot**
    This is an unofficial notice bot for Burdwan Raj College.
    
    
                                            source: [github](https://github.com/animeshxd/brcbot)
    """
    await db(_c.send_message(message.chat.id, text, reply_markup=buttons.about_button, disable_web_page_preview=True))


@client.on_message(filters=filters.private & filters.regex('About Burdwan Raj College') | filters.command('brc'), group=4)
@managed_event
async def about_brc(_c: Client, message: Message, *args, **kwargs):
    text = """
**Burdwan Raj College**
━━━━━━━━━━━━━━━━━━━━━━━
__Estd : 1881. Affiliated to The University of Burdwan__
__NAAC accredited with "B++" grade__

__Aftab House, Frazer Avenue, Burdwan - 713104__


→  `info@burdwanrajcollege.ac.in`

→  `0342` - `2565841`, `2657843`

→  [Burdwan Raj College](https://www.burdwanrajcollege.ac.in/)
    """
    await db(_c.send_message(
        message.chat.id, text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=buttons.about_button,
        disable_web_page_preview=True)
    )
