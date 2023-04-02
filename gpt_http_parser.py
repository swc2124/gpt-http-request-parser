"""HTTP Request Parsing Module.

This module was written by ChatGPT as a result of a series of questions asked
by the user. It provides functions for parsing raw HTTP requests, expressed as
Python data classes.

## Functions

- `parse_request(request_bytes: bytes) -> HTTPRequest`: Parses a raw HTTP
  request expressed as bytes and returns an `HTTPRequest` object.
- `parse_user_agent(user_agent_string: str) -> UserAgent`: Parses a User-Agent
  string and returns a `UserAgent` object.
- `parse_cookie(cookie_string: str) -> List[Cookie]`: Parses a Cookie string
  and returns a list of `Cookie` objects.
- `parse_authorization(authorization_string: str) -> Authorization`: Parses
  an Authorization string and returns an `Authorization` object.

## Data Classes

- `HTTPRequest`: Represents an HTTP request as a data class with attributes for
  the request method, path, headers, and body.
- `UserAgent`: Represents a User-Agent header as a data class with attributes
  for the browser name, version, and platform.
- `Cookie`: Represents a Cookie as a data class with attributes for the cookie
  name and value.
- `Authorization`: Represents an Authorization header as a data class with
  attributes for the authentication scheme and credentials.

"""
import dataclasses


# Custom exception classes for different types of malicious requests
class MalformedRequestException(Exception):
    pass


class MaliciousUserAgentException(MalformedRequestException):
    pass


class MaliciousCookieException(MalformedRequestException):
    pass


class MaliciousSecurityFieldException(MalformedRequestException):
    pass


class MaliciousAuthorizationException(MalformedRequestException):
    pass


@dataclasses.dataclass
class UserAgent:
    product: str
    version: str
    comment: str


@dataclasses.dataclass
class Cookie:
    name: str
    value: str


@dataclasses.dataclass
class SecurityField:
    field_name: str
    field_value: str


@dataclasses.dataclass
class Authorization:
    auth_type: str
    credentials: str


HeaderType = str | UserAgent | Cookie | SecurityField | Authorization


@dataclasses.dataclass
class HttpRequest:
    method: str
    uri: str
    http_version: str
    headers: dict[str, HeaderType | list[HeaderType]]
    body: str = dataclasses.field(default='')

    @property
    def bytes(self) -> bytes:
        request_line = f"{self.method} {self.uri} {self.http_version}"
        header_lines = [
            f"{name}: {value}"
            for name, value
            in self.headers.items()
            ]
        headers = "\r\n".join(header_lines)
        raw_request = f"{request_line}\r\n{headers}\r\n\r\n{self.body}"
        return raw_request.encode()


def parse_user_agent(user_agent_str: str) -> list[UserAgent]:
    user_agents = []
    user_agent_parts = user_agent_str.split(' ')
    for part in user_agent_parts:
        if '/' in part:
            product, version = part.split('/')
            comment = ''
        else:
            comment = part
        user_agents.append(UserAgent(product, version, comment))
    return user_agents


def parse_cookies(cookie_str: str) -> list[Cookie]:
    cookies = []
    cookie_pairs = cookie_str.split(';')
    for pair in cookie_pairs:
        name, value = pair.strip().split('=')
        cookies.append(Cookie(name, value))
    return cookies


def parse_security_fields(security_field_str: str) -> list[SecurityField]:
    security_fields = []
    fields = security_field_str.split(',')
    for field in fields:
        field_name, field_value = field.strip().split('=')
        security_fields.append(SecurityField(field_name, field_value))
    return security_fields


def parse_authorization(authorization_str: str) -> Authorization:
    auth_type, credentials = authorization_str.split(' ')
    return Authorization(auth_type, credentials)


def parse_http_request(raw_request: bytes) -> HttpRequest:
    try:
        request_lines = raw_request.decode().split('\r\n')
        method, uri, http_version = request_lines[0].split(' ')
        headers = {}
        idx = 1

        while request_lines[idx] != '':
            header_name, header_value = request_lines[idx].split(': ')
            if header_name.lower() == 'user-agent':
                header_value = parse_user_agent(header_value)
            elif header_name.lower() == 'cookie':
                header_value = parse_cookies(header_value)
            elif header_name.lower().startswith('sec-'):
                header_value = parse_security_fields(header_value)
            elif header_name.lower() == 'authorization':
                header_value = parse_authorization(header_value)
            headers[header_name] = header_value
            idx += 1

        body = '\r\n'.join(request_lines[(idx + 1):])
        return HttpRequest(method, uri, http_version, headers, body)
    except Exception as e:
        raise MalformedRequestException(f"Malformed request: {e}")
