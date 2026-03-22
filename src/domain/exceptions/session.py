"""Session-domain-related exceptions."""

from .base import AuthError


class SessionNotFoundError(AuthError):
    """Raised when a session is not found in the storage."""
