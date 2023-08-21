from pyrogram import filters, Client
from pyrogram.types import Message, ReplyKeyboardMarkup

from bot import client, db
from bot import university_notice_client
from bot.decorators.managed_event import managed_event
from bot.events.notices.events.notices import G
from bot.services.notice.buruniv import UGUniversityNoticeType, UGUniversityNoticeClient

buttons = ReplyKeyboardMarkup(
    [
        ["Examination"],
        ["Result"],
        ["Admission"],
        ["Menu"]
    ]
)


async def _handle_events(type: UGUniversityNoticeType,
                         message: Message,
                         tgcli: Client,
                         notice_cli: UGUniversityNoticeClient):
    loading = await tgcli.send_message(message.chat.id, "...")
    result = [f"<b>{message.text}</b>"]
    idx = 1
    async for i in notice_cli.iter_notices(type):
        result.append(f"{idx}. [{i.subject}]({i.fileurl})")
        idx += 1
    await loading.delete()
    if idx == 1:
        return await db(tgcli.send_message(message.chat.id, "No Notices were published.", reply_markup=buttons))
    await db(tgcli.send_message(message.chat.id, "\n".join(result), reply_markup=buttons, disable_web_page_preview=True))


@client.on_message(filters=filters.private & filters.regex('^Notices from University$'), group=G)
@managed_event
async def notices_buruniv(_c: Client, message: Message, *args, **kwargs):
    await db(client.send_message(message.chat.id, message.text, reply_markup=buttons))


@client.on_message(filters=filters.private & filters.regex('^Examination$'), group=G)
@managed_event
async def notices_buruniv_exam(_c: Client, message: Message, *args, **kwargs):
    await _handle_events(UGUniversityNoticeType.Examination, message, client, university_notice_client)


@client.on_message(filters=filters.private & filters.regex('^Result$'), group=G)
@managed_event
async def notices_buruniv_result(_c: Client, message: Message, *args, **kwargs):
    await _handle_events(UGUniversityNoticeType.Results, message, client, university_notice_client)


@client.on_message(filters=filters.private & filters.regex("^Admission"), group=G)
@managed_event
async def notices_buruniv_admission(_c: Client, message: Message, *args, **kwargs):
    await _handle_events(UGUniversityNoticeType.Admission, message, client, university_notice_client)
