from abc import ABC, abstractmethod
from typing import AsyncGenerator, Tuple


class NoticeClient(ABC):

    async def init(self):
        return await self.__aenter__()

    async def close(self):
        await self.__aexit__(None, None, None)

    @abstractmethod
    async def __aenter__(self) -> "NoticeClient":
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    async def fetch(self, *args, **kwargs) -> any:
        pass

    @abstractmethod
    async def iter_notices(self, *args, **kwargs) -> AsyncGenerator[any, None]:
        pass

    @abstractmethod
    async def iter_from(self, *args, **kwargs) -> AsyncGenerator[any, None]:
        pass
