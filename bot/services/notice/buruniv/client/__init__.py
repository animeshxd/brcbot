from typing import AsyncGenerator, Tuple

from bot.services.notice.interface import NoticeClient


class UniversityNoticeClient(NoticeClient):

    async def __aenter__(self) -> "NoticeClient":
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def fetch(self, page: int = 1, limit: int = 10, search: str = '') -> dict:
        pass

    async def iter_notices(self, search: str = '', limit_page: int = 0) -> AsyncGenerator[dict, None]:
        pass

    async def iter_from(self, date: str = '', file_id: str = '') -> AsyncGenerator[Tuple[int, dict], None]:
        pass
