from bot.services.notice import parser
from bot.services.notice.brc import raw

headers: dict = parser.parse_headers(raw.raw_headers)
req_data: dict = parser.parse_requests_data(raw.raw_data)
url_brc: str = 'https://burdwanrajcollege.ac.in/'


if __name__ == '__main__':
    print(headers)
    print(req_data)