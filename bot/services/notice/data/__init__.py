import dataclasses
from datetime import datetime, timedelta
from typing import Any

@dataclasses.dataclass
class Notice:
    fileurl: str = ''
    filename: str = ''
    date: datetime | None = None
    subject: str = ''
    extra: Any = ''