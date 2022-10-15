import logging

from pyrogram.client import Client
from bot.services.brc import Notices
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
db = Cache()
conv = Conversation()
notice = Notices()
