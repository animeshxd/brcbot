import logging
import os

from dotenv import load_dotenv

load_dotenv()

API_ID: int = int(os.getenv('API_ID'))
API_HASH: str = os.getenv('API_HASH')
BOT_TOKEN: str = os.getenv('BOT_TOKEN')
MONGO_SRV: str = os.getenv('MONGO_SRV')
LOG_LEVEL: int = getattr(logging, os.getenv('LOG_LEVEL', 'INFO'), logging.INFO)
PYROGRAM_LOG_LEVEL: int = getattr(logging, os.getenv('PYROGRAM_LOG_LEVEL', 'INFO'), LOG_LEVEL)

REDIS_HOST, REDIS_PORT = os.getenv("REDIS_URL").split(":")
REDIS_PORT = REDIS_PORT if REDIS_PORT else os.getenv('REDIS_PORT', 6379)
REDIS_USERNAME: str = os.getenv("REDIS_USERNAME", "default")
REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
PROFILE: int = int(os.getenv("PROFILE", "4"))


__all__ = ["API_ID", "API_HASH", "BOT_TOKEN", "MONGO_SRV", "LOG_LEVEL", "REDIS_HOST", "REDIS_PORT", "REDIS_USERNAME",
           "REDIS_PASSWORD", "PROFILE"]
