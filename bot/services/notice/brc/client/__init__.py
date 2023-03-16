from datetime import datetime
from typing import AsyncGenerator, Tuple
from urllib.parse import urljoin

from aiohttp import CookieJar
from aiohttp.client import ClientSession, ClientTimeout

from bot.services.notice.brc.base import headers, url_brc
from bot.services.notice.data import Notice
from bot.services.notice.interface import NoticeClient


class CollegeNoticeClient(NoticeClient):
    TAG = 'BRC'
    cookie_jar = CookieJar(unsafe=True)

    def __init__(self):
        pass

    async def __aenter__(self) -> "NoticeClient":
        self.session = ClientSession(base_url=url_brc, headers=headers, timeout=ClientTimeout(total=20))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def fetch(self, page: int = 1, limit: int = 10, search: str = '',  *args, **kwargs) -> dict:
        """

        :param page:
        :param limit:
        :param search: stringlike date in YYYY-mm-dd format / string query
        :return: dict
        """
        assert page > 0, f'expected (page > 0) got page={page}'
        req_data = {
            'draw': '0',
            'columns[0][data]': 'dop',
            'columns[0][name]': '',
            'columns[0][searchable]': 'true',
            'columns[0][orderable]': 'true',
            'columns[0][search][value]': '',
            'columns[0][search][regex]': 'false',
            'columns[1][data]': 'subject',
            'columns[1][name]': '',
            'columns[1][searchable]': 'true',
            'columns[1][orderable]': 'true',
            'columns[1][search][value]': '',
            'columns[1][search][regex]': 'false',
            'order[0][column]': '0',
            'order[0][dir]': 'desc',
            'start': (page - 1) * 10,
            'length': limit,
            'search[value]': search,
            'search[regex]': 'true'
        }

        async with self.session.post('/scripts/notices', data=req_data) as response:
            if not response.ok:
                raise RuntimeError(f"response status not ok POST[{response.status}][{response.url}]")

            json_data: dict = await response.json(content_type=None)
            data = json_data.get("data", None)
            if data is None:
                raise ValueError("data: [] is missing or empty")

            return json_data

    async def iter_notices(self, search: str = '', limit_page: int = 0,  *args, **kwargs) -> AsyncGenerator[Notice, None]:
        page = 1
        limit = 10
        _data = await self.fetch(page=page, limit=limit, search=search)
        data = _data.get('data', [])
        if not data:
            return
        for i in data:
            filename = i.get('filename', '')
            fileurl=urljoin("https://burdwanrajcollege.ac.in/docs/notices/", filename)
            _ = i.get('don', '')
            _date = datetime.strptime(_, "%Y-%m-%d") if _ else None
            subject = i.get("subject", '')
            yield Notice(fileurl, filename, _date, subject, extra=i.get('dop', ''))
        if _data['recordsTotal'] <= limit:
            return
        while True:
            # print('_')
            if page >= limit_page:
                break
            page += 1
            _data = await self.fetch(page=page, search=search)
            data = _data['data']
            if not data:
                break
            for i in data:
                filename = i.get('filename', '')
                fileurl=urljoin("https://burdwanrajcollege.ac.in/docs/notices/", filename)
                _ = i.get('don', '')
                _date = datetime.strptime(_, "%Y-%m-%d") if _ else None
                subject = i.get("subject", '')
                yield Notice(fileurl, filename, _date, subject, extra=i.get('dop', ''))
        return

    async def iter_after(self, date: str | datetime = '', file_id: str = '', *args, **kwargs) -> AsyncGenerator[Tuple[int, Notice], None]:
        assert date or file_id, "both params are empty, one of required"
        # assert not (date and file_id), "both params are full, only one of required"
        if isinstance(date, datetime):
            date = datetime.strftime(date, "%Y-%m-%d")
        _data = await self.fetch()
        data = _data['data']
        if not data:
            return
        found = False
        for index, i in zip(range(len(data), -1, -1), reversed(data)):
            if not found:
                if date and file_id:
                    if i['don'] == date and i['filename'] == file_id:
                        found = True
                        continue
                else:
                    if date:
                        # print(f'{i["don"]} == {date}')
                        # print(i['don'] == date)
                        if i['don'] == date:
                            found = True
                            # yield i
                            continue
                    if file_id:
                        if i['filename'] == file_id:
                            found = True
                            # yield i
                            continue
            if found:
                filename = i.get('filename', '')
                fileurl=urljoin("https://burdwanrajcollege.ac.in/docs/notices/", filename)
                _date = datetime.strptime(i.get('don', ''), "%Y-%m-%d")
                subject = i.get("subject", '')
                yield index, Notice(fileurl, filename, _date, subject, extra=i.get('dop', ''))
