"""HTTP Request Parsing Test Module.

This module was written by ChatGPT as a result of a series of questions asked
by the user. It provides a Hypothesis strategy for generating valid HTTP
requests for testing purposes.

## Hypothesis Strategies

- `http_request_bytes()`: Generates random bytes representing an HTTP request.
- `http_request_dataclass()`: Generates random instances of the `HTTPRequest`
  data class.
- `valid_json()`: Generates random strings representing valid JSON objects.

"""
import json
import string

from hypothesis import strategies as st

from gpt_http_parser import HttpRequest

methods = st.sampled_from(
    ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']
    )
http_versions = st.sampled_from(['HTTP/1.0', 'HTTP/1.1', 'HTTP/2'])

common_path_segments = st.sampled_from(
    [
        'api',
        'v1',
        'v2',
        'users',
        'products',
        'items',
        'search',
        'auth',
        'login',
        'logout',
        'register'
        ]
    )
path = st.lists(common_path_segments, min_size=1, max_size=5).map('/'.join)

query_key = st.sampled_from(['page', 'results', 'sort'])
query_value = st.one_of(
    st.integers(min_value=1, max_value=100),
    st.sampled_from(['asc', 'desc'])
    )
query = st.lists(st.tuples(query_key, query_value), min_size=0, max_size=3)

uris = st.builds(
    lambda p, q: f"{p}?{'&'.join(f'{k}={v}' for k, v in q)}" if q else p,
    path, query
)

header_names_values = [
    (
        'Accept',
        'text/html,application/xhtml+xml,application/xml;q=0.9',
        'application/json',
        'application/xml',
        'application/octet-stream'
        ),
    (
        'Accept-Charset',
        'utf-8, iso-8859-1;q=0.5',
        'utf-8',
        'iso-8859-1'
        ),
    (
        'Accept-Encoding',
        'gzip, deflate, br',
        'gzip, deflate',
        'br'
        ),
    (
        'Accept-Language',
        'en-US,en;q=0.5',
        'en-US',
        'en-GB',
        'fr-FR'
        ),
    (
        'Authorization',
        'Bearer <token>',
        'Basic <credentials>',
        'OAuth <token>'),
    (
        'Cache-Control',
        'no-cache',
        'no-store',
        'must-revalidate',
        'public',
        'max-age=3600',
        'private',
        'no-store',
        'no-cache',
        'must-revalidate'
        ),
    (
        'Connection',
        'keep-alive',
        'close'
        ),
    (
        'Content-Length',
        '348',
        '1024',
        '2048'
        ),
    (
        'Content-Type',
        'application/json',
        'application/xml',
        'text/plain'
        ),
    (
        'Cookie',
        'sessionId=38afes7a8; _ga=GA1.2.156011732.1578476096',
        'SESSION_ID=38AFES7A8'
        ),
    (
        'Date',
        'Mon, 18 Oct 2021 16:45:00 GMT',
        'Tue, 19 Oct 2021 12:00:00 GMT'
        ),
    (
        'ETag',
        '"12345678901234567890"',
        '"abcdef0123456789"'
        ),
    (
        'Host',
        'www.example.com',
        'api.example.com',
        'test.example.com'),
    (
        'If-Modified-Since',
        'Sat, 29 Oct 2019 19:43:31 GMT',
        'Sun, 30 Oct 2019 19:43:31 GMT'
        ),
    (
        'If-None-Match',
        '"737060cd8c284d8af7ad3082f209582d"',
        '"c4ca4238a0b923820dcc509a6f75849b"'),
    (
        'Referer',
        'http://www.example.com/previous-page',
        'https://www.example.com/new-page'),
    (
        'User-Agent',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', # noqa
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36', # noqa
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko' # noqa
        ),
    (
        'X-Forwarded-For',
        '192.168.1.1',
        '10.0.0.1',
        '172.16.0.1'
        ),
    (
        'X-Forwarded-Proto',
        'https',
        'http'
        ),
    ]

header_names_values = st.sampled_from(
    [(itm[0], v) for itm in header_names_values for v in itm[1:]]
    )
headers = st.lists(header_names_values, min_size=1, max_size=10).map(dict)

json_body = st.recursive(
    st.one_of(
        st.none(),
        st.booleans(),
        st.floats(),
        st.integers(),
        st.text(),
        ),
    lambda children: st.lists(children) | st.dictionaries(
        st.text(alphabet=string.printable), children
        ),
    max_leaves=100,
    )

body = json_body.map(json.dumps)

http_request_strategy = st.builds(
    HttpRequest,
    method=methods,
    uri=uris,
    http_version=http_versions,
    headers=headers,
    body=body | st.sampled_from([''])
    )
