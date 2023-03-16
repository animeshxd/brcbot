from dataclasses import dataclass
from datetime import datetime


@dataclass
class MFile:
    _id: str
    id: str = ''
    date: datetime| None = None
    file_id: str = ''

    def __post_init__(self):
        self.id = str(self._id)

