from enum import Enum


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"

    def __str__(self) -> str:
        return self.value


DEFAULT_HEADER = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "APIArtisan",
}


class HTTPConfig:
    def __init__(
        self,
        url: str = "https://example.com",
        method: HttpMethod = HttpMethod.GET,
        headers: dict = DEFAULT_HEADER,
        body: dict = {},
    ) -> None:
        self.url = url
        self.method = method
        self.headers = headers
        self.body = body

    def to_dict(self) -> dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: dict) -> "HTTPConfig":
        data = data.copy()
        data["method"] = HttpMethod(data.get("method", HttpMethod.GET))
        return cls(**data)

    def set_url(self, url: str) -> None:
        self.url = url

    def set_method(self, method: HttpMethod) -> None:
        self.method = method

    def set_headers(self, headers: dict) -> None:
        self.headers = headers

    def set_body(self, body: dict) -> None:
        self.body = body
