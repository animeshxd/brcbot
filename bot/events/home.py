from pyrogram import filters, Client
from pyrogram.raw.types import UpdateBotStopped
from pyrogram.types import Message, ReplyKeyboardMarkup

from bot import client, db
from bot.decorators.managed_event import managed_event
from bot.decorators.on_raw_type import on_raw_type
from bot.events import buttons
from bot.mongo import mongo


@client.on_message(filters=filters.private & filters.command('start'), group=1)
@managed_event
async def start(_c: Client, message: Message, *args, **kwargs):
    result = await mongo.user_find(message.chat.id)
    if not result:
        button = ReplyKeyboardMarkup(
            [
                ['Yes! Subscribe'],
                ['No']
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await db(_c.send_message(message.chat.id, "Would you like to subscribe for notices?", reply_markup=button))
        await mongo.user_add(message.chat.id)
    else:
        await db(_c.send_message(message.chat.id, "Welcome Back!", reply_markup=buttons.home_buttons))


@client.on_raw_update()
@on_raw_type(UpdateBotStopped)
async def bot_stopped(_c: Client, update: UpdateBotStopped, *args, **kwargs):
    await mongo.user_update(update.user_id, stopped=update.stopped)


@client.on_message(group=1, filters=filters.private & filters.command('home') | filters.regex('Home'))
@managed_event
async def home(_c: Client, message: Message, *args, **kwargs):
    await db(_c.send_message(message.chat.id, 'Settings', reply_markup=buttons.home_buttons))
