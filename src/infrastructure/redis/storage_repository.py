"""Interface for base storage services."""

import json
from dataclasses import asdict
from typing import TYPE_CHECKING

from redis.exceptions import ConnectionError, TimeoutError
from src.domain.interfaces.storage_repository import IStorageRepository

from .exceptions import RedisError
from .models import Session

if TYPE_CHECKING:
    from redis.asyncio import Redis


class RedisStorageRepository(IStorageRepository):
    def __init__(self, client: "Redis"):
        self.client = client

    def _key(self, refresh_token: str) -> str:
        return f"session:{refresh_token}"

    def _dumps(self, value: Session) -> str:
        return json.dumps(asdict(value))

    def _loads(self, value: str) -> Session:
        return Session(**json.loads(value))

    async def create(
        self,
        user_id: str,
        refresh_token: str,
        ip_address: str,
        ttl: int,
    ) -> Session:
        """Create a new user in the storage and return the user ID."""

        session = Session(
            user_id=user_id,
            ip_address=ip_address,
            refresh_token=refresh_token,
            expires_in=ttl,
        )

        try:
            await self.client.set(
                self._key(refresh_token), self._dumps(session), ex=ttl
            )
        except (ConnectionError, TimeoutError) as e:
            raise RedisError("Failed to communicate with Redis storage") from e

        return session

    async def get(self, refresh_token: str) -> Session | None:
        """Get a user from the storage by their refresh token."""

        try:
            data = await self.client.get(self._key(refresh_token))
        except (ConnectionError, TimeoutError) as e:
            raise RedisError("Failed to communicate with Redis storage") from e

        if data is None:
            return None

        return self._loads(data)

    async def delete(self, refresh_token: str) -> None:
        """Delete a user from the storage by their refresh token."""

        try:
            await self.client.delete(self._key(refresh_token))
        except (ConnectionError, TimeoutError) as e:
            raise RedisError("Failed to communicate with Redis storage") from e
