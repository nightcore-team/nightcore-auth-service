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

    def _session_key(self, refresh_token: str) -> str:
        return f"session:{refresh_token}"

    def _user_sessions_key(self, user_id: str) -> str:
        return f"user_sessions:{user_id}"

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
            async with self.client.pipeline(transaction=True) as pipe:
                pipe.set(
                    self._session_key(refresh_token),
                    self._dumps(session),
                    ex=ttl,
                )
                pipe.sadd(self._user_sessions_key(user_id), refresh_token)
                pipe.expire(self._user_sessions_key(user_id), ttl)

                await pipe.execute(raise_on_error=True)

        except (ConnectionError, TimeoutError) as e:
            raise RedisError("Failed to communicate with Redis storage") from e

        return session

    async def get(self, refresh_token: str) -> Session | None:
        """Get a user from the storage by their refresh token."""

        try:
            data = await self.client.get(self._session_key(refresh_token))
        except (ConnectionError, TimeoutError) as e:
            raise RedisError("Failed to communicate with Redis storage") from e

        if data is None:
            return None

        return self._loads(data)

    async def delete(
        self, user_id: str, refresh_token: str | None = None
    ) -> int:
        """Delete a user from the storage by their refresh token."""

        try:
            if refresh_token:
                async with self.client.pipeline(transaction=True) as pipe:
                    pipe.delete(self._session_key(refresh_token))
                    pipe.srem(self._user_sessions_key(user_id), refresh_token)
                    results = await pipe.execute(raise_on_error=True)

                return results[0]

            else:
                user_sessions_key = self._user_sessions_key(user_id)

                tokens = await self.client.smembers(user_sessions_key)  # type: ignore

                if not tokens:
                    return 0

                session_keys = [self._session_key(token) for token in tokens]  # type: ignore

                async with self.client.pipeline(transaction=True) as pipe:
                    pipe.delete(*session_keys)
                    pipe.delete(user_sessions_key)

                    results = await pipe.execute(raise_on_error=True)

                return results[0]

        except (ConnectionError, TimeoutError) as e:
            raise RedisError("Failed to communicate with Redis storage") from e
