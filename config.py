import logging
import os

from dotenv import load_dotenv

load_dotenv()

API_ID: int = int(os.getenv('API_ID'))
API_HASH: str = os.getenv('API_HASH')
BOT_TOKEN: str = os.getenv('BOT_TOKEN')
MONGO_SRV: str = os.getenv('MONGO_SRV')
LOG_LEVEL: int = getattr(logging, os.getenv('LOG_LEVEL', 'INFO'), logging.INFO)

REDIS_HOST, REDIS_PORT = os.getenv("REDIS_URL").split(":")
REDIS_USERNAME: str = os.getenv("REDIS_USERNAME", "default")
REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
PROFILE: int = int(os.getenv("PROFILE", "4"))

__all__ = ["API_ID", "API_HASH", "BOT_TOKEN", "MONGO_SRV", "LOG_LEVEL", "REDIS_HOST", "REDIS_PORT", "REDIS_USERNAME",
           "REDIS_PASSWORD", "PROFILE"]
