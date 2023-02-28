import datetime


def parse_headers(raw_headers) -> dict:
    headers = {}

    for i in raw_headers.strip().split("\n"):
        h = i.split(": ")
        headers[h[0]] = h[1].strip()
    return headers


def parse_requests_data(raw_data) -> dict:
    data = {}
    for i in raw_data.strip().split('\n'):
        raw = i.replace("\t", " ").strip().split(" ")
        if len(raw) < 2:
            print(raw)
            raise ValueError('Invalid request data')
        data[raw[0]] = raw[1].replace('"', '')
    return data


def parse_date(date: str):
    return datetime.datetime.strptime(date, '%Y-%m-%d')  # ` 2022-07-04
