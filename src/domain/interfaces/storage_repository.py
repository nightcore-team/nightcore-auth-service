"""Interface for base storage services."""

from typing import Any, Protocol


class IStorageRepository(Protocol):
    async def create(
        self, user_id: str, refresh_token: str, ip_address: str, ttl: int
    ) -> Any:
        """Create a new user in the storage and return the user ID."""
        ...

    async def get(self, refresh_token: str) -> Any | None:
        """Get a user from the storage by their ID."""
        ...

    async def delete(
        self, user_id: str, refresh_token: str | None = None
    ) -> int:
        """Delete a user from the storage by their ID."""
        ...

    # async def update(self, user_id: str, user_data: dict[str, str]) -> None:
    #     """Update a user in the storage by their ID."""
    #     ...
