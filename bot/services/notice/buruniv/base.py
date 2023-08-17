from bot.services.notice import parser


raw_headers = """
Host: buruniv.ac.in
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Origin: https://buruniv.ac.in
Connection: keep-alive
Referer: https://buruniv.ac.in/bunew/Template.php?page=NOT_CATEGORY&subpage=EXAM_UG
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
"""

headers = parser.parse_headers(raw_headers)