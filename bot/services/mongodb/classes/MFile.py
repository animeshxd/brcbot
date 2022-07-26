from dataclasses import dataclass


@dataclass
class MFile:
    _id: str
    id: str = ''
    date: str = ''
    file_id: str = ''

    def __post_init__(self):
        self.id = str(self._id)

