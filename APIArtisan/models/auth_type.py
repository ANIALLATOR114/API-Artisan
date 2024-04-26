import enum


class AuthType(str, enum.Enum):
    BASIC = "Basic"
    OAUTH = "OAuth"
    BEARER = "Bearer"
    NONE = "None"
