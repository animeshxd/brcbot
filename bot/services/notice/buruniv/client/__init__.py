import enum
import logging
from typing import AsyncGenerator, Tuple
from urllib.parse import urljoin

from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup, ResultSet, Tag
from bot.services.notice.data import Notice

from bot.services.notice.interface import NoticeClient
from bot.services.notice.buruniv.base import headers

class NoticeType(enum.Enum):
    Examination = "EXAM_UG"
    Admission = "ADMN_UG"
    Results = "EXRS_UG"

log = logging.getLogger(__name__)
class UGUniversityNoticeClient(NoticeClient):
    buruniv = "https://buruniv.ac.in"
    _buruniv = "https://buruniv.ac.in/bunew/"

    async def __aenter__(self) -> "NoticeClient":
        self.session = ClientSession(base_url=self.buruniv, headers=headers, timeout=ClientTimeout(total=20))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def fetch(self, type: NoticeType) -> ResultSet[Tag]:
        async with self.session.post("/bunew/AllFunctions.php", data = {"parentmenu": "NOT_CATEGORY", "childmenu": type.value}) as response:
            if not response.ok:
                raise RuntimeError(f"response status not ok POST[{response.status}][{response.url}]")
            html = await response.text()
            soup = BeautifulSoup(html, 'lxml')
            data = soup.select(".content_list > ol > li > a")

            if not data:
                raise ValueError("data is missing or empty")
            
            return data

    async def iter_notices(self, type: NoticeType, search: str | None = None) -> AsyncGenerator[Notice, None]:
        result = await self.fetch(type)
        for i in result:
            subject = i.text.strip()
            fileurl=urljoin(self._buruniv, i.get('href', ''))
            if search:
                if search.lower() in subject.lower():
                    yield Notice(fileurl, subject=subject)
            else:
                yield Notice(fileurl, subject=subject)


    async def iter_from(self, date: str = '', file_id: str = '') -> AsyncGenerator[Tuple[int, dict], None]:
        raise NotImplementedError
