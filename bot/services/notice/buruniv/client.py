import enum
import logging
from typing import AsyncGenerator, Tuple
from urllib.parse import urljoin

from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup, ResultSet, Tag
from bot.services.notice.data import Notice

from bot.services.notice.interface import NoticeClient, NoticeType
from bot.services.notice.buruniv.base import headers
from bot.services.notice.parser import get_filename

class UGUniversityNoticeType(enum.Enum):
    Examination = "EXAM_UG"
    Admission = "ADMN_UG"
    Results = "EXRS_UG"


log = logging.getLogger(__name__)


class UGUniversityNoticeClient(NoticeClient):
    TAG = 'buruniv'
    buruniv = "https://buruniv.ac.in"
    _buruniv = "https://buruniv.ac.in/bunew/"
    """
    https://www.buruniv.ac.in/Demo/Template.php?menu=NOT_EXAM&submenu=EXAM_UG
    https://www.buruniv.ac.in/Demo/Template.php?menu=NOT_EXAM&submenu=EXAM_PS
    
    """

    async def __aenter__(self) -> "NoticeClient":
        self.session = ClientSession(base_url=self.buruniv, headers=headers, timeout=ClientTimeout(total=20))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def fetch(self, type: UGUniversityNoticeType,  *args, **kwargs) -> ResultSet[Tag]:
        async with self.session.get("/Demo/Template.php",
                                    params={"menu": "NOT_EXAM", "submenu": type.value}) as response:
            if not response.ok:
                raise RuntimeError(f"response status not ok POST[{response.status}][{response.url}]")
            html = await response.text()
            soup = BeautifulSoup(html, 'lxml')
            data = soup.select("ol.notice_content_list > li > a")

            if not data:
                raise ValueError("data is missing or empty")

            return data

    async def iter_notices(self, type: UGUniversityNoticeType, search: str | None = None,  *args, **kwargs) -> AsyncGenerator[Notice, None]:
        result = await self.fetch(type)
        for i in result:
            subject = i.text.strip()
            filename = i.get('href', '')
            fileurl = urljoin(self._buruniv, filename)
            filename = get_filename(fileurl)
            if search:
                if search.lower() in subject.lower() or search.lower() in fileurl.lower():
                    yield Notice(fileurl, filename, subject=subject)

            else:
                yield Notice(fileurl, filename, subject=subject)

    async def iter_after(self, file_id: str, type: UGUniversityNoticeType,  *args, **kwargs) -> AsyncGenerator[Tuple[int, Notice], None]:
        found = False
        result = await self.fetch(type=type)
        for index, i in zip(range(len(result), -1, -1), reversed(result)):
            subject = i.text.strip()
            filename = i.get('href', '')
            fileurl = urljoin(self._buruniv, filename)
            filename = get_filename(fileurl)
            # log.debug(f" {filename == file_id} {file_id, filename}")
            if found:
                # log.debug(f" {filename == file_id} {file_id, filename}")
                yield index, Notice(fileurl, filename, subject=subject)
            if file_id == filename:
                found = True
                continue









