from aiohttp import CookieJar
from aiohttp.client import ClientSession, ClientTimeout

from bot.services.brc.base import headers, url_brc


class Notices:
    cookie_jar = CookieJar(unsafe=True)

    def __init__(self):
        pass

    async def init(self):
        await self.__aenter__()

    async def close(self):
        await self.__aexit__(None, None, None)

    async def __aenter__(self):
        self.session = ClientSession(base_url=url_brc, headers=headers, timeout=ClientTimeout(total=20))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def fetch(self, page: int = 1, limit: int = 10, search: str = '') -> dict:
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

    async def iter_notices(self, search: str = '', limit_page: int = 0):
        page = 1
        limit = 10
        _data = await self.fetch(page=page, limit=limit, search=search)
        data = _data.get('data', [])
        if not data:
            return
        for i in data:
            yield i
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
                yield i
        return
