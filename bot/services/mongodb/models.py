from dataclasses import dataclass


@dataclass()
class MUser:
    id: int
    stopped: bool
    subscribed: bool
