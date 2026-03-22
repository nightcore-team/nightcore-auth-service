"""Token-related exceptions."""

from .base import AuthError


class RefreshTokenNotProvidedError(AuthError):
    """Raised when a refresh token is not provided for refreshing the access token."""  # noqa: E501


class TokenRevokedError(AuthError):
    """Raised when a refresh token is revoked or invalid."""
