import enum

from typing import Any


class HttpMethod(enum.Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"

    def valid_method(value: Any):
        valid_values = [member.value for member in HttpMethod]
        return value in valid_values
