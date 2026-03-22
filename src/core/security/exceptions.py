"""JWT-related exceptions."""

from src.domain.exceptions.base import AuthError


class TokenError(AuthError):
    pass


class InvalidTokenError(TokenError):
    pass


class TokenExpiredError(TokenError):
    pass
