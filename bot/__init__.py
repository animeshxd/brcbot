import logging

from pyrogram.client import Client

from bot.const import profiles
from bot.services.notice.brc import CollegeNoticeClient
from bot.services.cache import Cache
from bot.services.conversation import Conversation
from config import *

logging.basicConfig(level=LOG_LEVEL)
client = Client(
    'pyro',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)
db = Cache(PROFILE == profiles.DEVELOPMENT)
conv = Conversation()
notice = CollegeNoticeClient()
