from abc import ABC, abstractmethod
from typing import AsyncGenerator, Tuple


class NoticeClient(ABC):

    async def init(self):
        await self.__aenter__()

    async def close(self):
        await self.__aexit__(None, None, None)

    @abstractmethod
    async def __aenter__(self) -> "NoticeClient":
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    async def fetch(self, page: int = 1, limit: int = 10, search: str = '') -> dict:
        pass

    @abstractmethod
    async def iter_notices(self, search: str = '', limit_page: int = 0) -> AsyncGenerator[dict, None]:
        pass

    @abstractmethod
    async def iter_from(self, date: str = '', file_id: str = '') -> AsyncGenerator[Tuple[int, dict], None]:
        pass
