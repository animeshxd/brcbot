import logging
import os

API_ID: int = int(os.getenv('API_ID'))
API_HASH: str = os.getenv('API_HASH')
BOT_TOKEN: str = os.getenv('BOT_TOKEN')
MONGO_SRV: str = os.getenv('MONGO_SRV')
LOG_LEVEL: int = getattr(logging, os.getenv('LOG_LEVEL', 'INFO'), logging.INFO)