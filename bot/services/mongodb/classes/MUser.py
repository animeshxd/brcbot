from dataclasses import dataclass


@dataclass()
class MUser:
    _id: int
    id: int = None
    stopped: bool = True
    subscribed: bool = False
    notified: bool = False

    def __post_init__(self):
        self.id = self._id
