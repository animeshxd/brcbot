import dataclasses
from datetime import datetime, timedelta

@dataclasses.dataclass
class Notice:
    fileurl: str = ''
    date: datetime | None = None
    subject: str = ''
    extra: any = None