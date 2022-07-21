from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from bot import client, db
from bot.decorators.managed_event import managed_event
from bot.events import buttons


@client.on_message(group=3, filters=filters.private & filters.command('menu') | filters.regex('Menu|Back$'))
@managed_event
async def home(_c: Client, message: Message, *args, **kwargs):
    await db(client.send_message(message.chat.id, 'Menu', reply_markup=buttons.menu_buttons))


@client.on_message(group=3, filters=filters.private & filters.command('admission') | filters.regex('Online Admission'))
@managed_event
async def admission(_c: Client, message: Message, *args, **kwargs):
    text = """
    <b>Online Admission</b>
    <a href="http://onlineadmissionbrc.org.in">Online admission (BA/BSc/BCom)</a>
    <a href="http://bbabcaonlineadmissionbrc.org.in">Online admission (BBA/BCA)</a>
    """
    await db(client.send_message(message.chat.id, text, parse_mode=ParseMode.HTML, reply_markup=buttons.menu_buttons))
