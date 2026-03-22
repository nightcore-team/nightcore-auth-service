"""Redis-related exceptions."""

from src.domain.exceptions.base import AuthError


class RedisError(AuthError):
    """Base class for Redis-related errors."""
