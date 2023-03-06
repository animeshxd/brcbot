import datetime
from os import path


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


def get_filename(url):
    fragment_removed = url.split("#")[0]  # keep to left of first #
    query_string_removed = fragment_removed.split("?")[0]
    scheme_removed = query_string_removed.split("://")[-1].split(":")[-1]
    if scheme_removed.find("/") == -1:
        return ""
    return path.basename(scheme_removed)
