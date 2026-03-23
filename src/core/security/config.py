"""JWT configuration."""

import base64

from pydantic import field_validator

from src.core.config.env import BaseEnvConfig


class Config(BaseEnvConfig):
    """JWT configuration."""

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    @field_validator("JWT_PRIVATE_KEY", mode="before")
    @classmethod
    def decode_private_key(cls, v: str) -> str:
        """Decode the base64-encoded private key."""

        return base64.b64decode(v).decode()

    @field_validator("JWT_PUBLIC_KEY", mode="before")
    @classmethod
    def decode_public_key(cls, v: str) -> str:
        """Decode the base64-encoded public key."""

        return base64.b64decode(v).decode()
