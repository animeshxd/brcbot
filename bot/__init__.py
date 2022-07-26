import logging

from pyrogram.client import Client
from bot.services.brc import Notices
from bot.services.cache import Cache
from bot.services.conversation import Conversation
import config as V

logging.basicConfig(level=V.LOG_LEVEL)
client = Client(
    'pyro',
    api_id=V.API_ID,
    api_hash=V.API_HASH,
    bot_token=V.BOT_TOKEN,
)
db = Cache()
conv = Conversation()
notice = Notices()
