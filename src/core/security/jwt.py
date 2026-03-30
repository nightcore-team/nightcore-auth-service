"""JWT token service implementation."""

import secrets
import uuid
from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from src.domain.interfaces.token import ITokenService

from .config import Config as JWTConfig
from .exceptions import InvalidTokenError


class JWTTokenService(ITokenService):
    def __init__(
        self,
        config: JWTConfig,
    ):
        self.config = config

    def create_access_token(self, user_id: str) -> str:
        """Create access token for user."""

        return self.sign({"sub": user_id})

    def create_refresh_token(self) -> str:
        """Create refresh token for user."""

        return str(uuid.uuid5(uuid.NAMESPACE_DNS, secrets.token_urlsafe(64)))

    def sign(self, payload: dict[str, str | int]) -> str:
        """Create and sign JWT token."""

        now = datetime.now(UTC)
        full_payload = payload.copy()
        full_payload.update(
            {
                "iat": int(now.timestamp()),
                "exp": int(
                    (
                        now
                        + timedelta(
                            minutes=self.config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
                        )
                    ).timestamp()
                ),
            }
        )
        try:
            return jwt.encode(
                full_payload,
                self.config.JWT_PRIVATE_KEY,
                algorithm=self.config.JWT_ALGORITHM,
            )
        except JWTError as e:
            raise InvalidTokenError() from e
