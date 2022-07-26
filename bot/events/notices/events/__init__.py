from functools import partial
from bot.events.notices.base import base as _b
from bot import db, notice, conv
from bot.decorators.suppress_error import suppress_error
from bot.decorators.delete_from_sender import delete_from_sender
base = partial(_b, notice=notice, cache=db, conv=conv)
surpress_error = partial(suppress_error, cache=db)
delete_from_sender = partial(delete_from_sender, cache=db)
