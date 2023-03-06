import dataclasses
from datetime import datetime, timedelta

@dataclasses.dataclass
class Notice:
    fileurl: str = ''
    filename: str = ''
    date: datetime | None = None
    subject: str = ''
    extra: any = None