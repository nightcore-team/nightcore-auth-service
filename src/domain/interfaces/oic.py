"""Interface for base IOC services."""

from typing import Protocol

from ..entities.token import Token
from .oauth_provider import IOAuthProvider
from .storage_repository import IStorageRepository
from .token import ITokenService


class IOICService(Protocol):
    """Interface for services that can be used in the OIC flow."""

    oauth_provider: IOAuthProvider
    token_service: ITokenService
    storage: IStorageRepository

    async def login(self, code: str, ip_address: str) -> Token:
        """Start the OIC flow by redirecting the user to the OAuth provider."""
        ...

    async def refresh(self, refresh_token: str, ip_address: str) -> Token:
        """Refresh the user's access token using the refresh token."""
        ...

    async def logout(self, refresh_token: str) -> None:
        """Logout the user by deleting their data from the storage."""
        ...
