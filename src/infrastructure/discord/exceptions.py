"""Discord-related exceptions."""

from src.domain.exceptions.base import AuthError


class DiscordAuthError(AuthError):
    """Base class for Discord authentication errors."""


class AuthorizationCodeNotProvidedError(DiscordAuthError):
    """Raised when the authorization code is not provided in the callback."""


class DiscordAPIError(DiscordAuthError):
    """Raised when there is an error while communicating with the Discord API."""  # noqa: E501


class UserInfoRetrievalError(DiscordAuthError):
    """Raised when there is an error while retrieving user info from Discord."""  # noqa: E501


class TokenExchangeError(DiscordAuthError):
    """Raised when there is an error while exchanging the authorization code for tokens."""  # noqa: E501
