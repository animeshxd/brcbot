from pyrogram import Client, filters
from pyrogram.types import Message

from bot import db, client
from bot.decorators.managed_event import managed_event
from bot.events import buttons
from bot.mongo import mongo


@client.on_message(filters=filters.private & filters.regex('Settings'), group=6)
@managed_event
async def settings(_c: Client, message: Message, *args, **kwargs):
    user = await mongo.user_find(message.chat.id)
    if user:
        subscribed = user.subscribed
    else:
        subscribed = False
    await db(client.send_message(message.chat.id, 'Menu', reply_markup=buttons.setting_button(subscribed)))


@client.on_message(filters=filters.private & filters.regex('Subscribe') | filters.command(['subscribe']), group=2)
@managed_event
async def subscribe(_c: Client, message: Message, *args, **kwargs):
    await mongo.user_subscribe(message.chat.id)
    await db(_c.send_message(message.chat.id, 'Done, [Subscribed]', reply_markup=buttons.setting_button(True)))


@client.on_message(filters=filters.private & filters.command('unsubscribe') | filters.regex('Unsubscribe'), group=2)
@managed_event
async def unsubscribe(_c: Client, message: Message, *args, **kwargs):
    await mongo.user_unsubscribe(message.chat.id)
    await db(message.reply('Done, [Unsubscribed]', reply_markup=buttons.setting_button(False)))


@client.on_message(filters=filters.private & filters.command('clear') | filters.regex('Clear History'), group=2)
@managed_event
async def clear_history(_c: Client, message: Message, *args, **kwargs):
    clear = await db.takeout(message.chat.id)
    user = await mongo.user_find(message.chat.id)
    if clear:
        await client.delete_messages(message.chat.id, message_ids=clear)
        await db(client.send_message(
            message.chat.id, 'Successfully Cleared',
            reply_markup=buttons.setting_button(user.subscribed)
            )
        )
    else:
        await db(_c.send_message(message.chat.id, "We have nothing to Clear", reply_markup=buttons.setting_button(user.subscribed)))
