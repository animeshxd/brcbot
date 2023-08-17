from functools import partial
from bot.events.notices.base import handle as _b
from bot import db, college_notice_client, conv
from bot.decorators.suppress_error import suppress_error
from bot.decorators.delete_from_sender import delete_from_sender
handle = partial(_b, notice=college_notice_client, cache=db, conv=conv)
suppress_error = partial(suppress_error, cache=db)
delete_from_sender = partial(delete_from_sender, cache=db)
