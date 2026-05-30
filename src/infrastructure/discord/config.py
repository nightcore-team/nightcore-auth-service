"""Discord authentication configuration."""

from src.core.config.env import BaseEnvConfig


class Config(BaseEnvConfig):
    DISCORD_AUTH_CLIENT_ID: str
    DISCORD_AUTH_CLIENT_SECRET: str
    DISCORD_AUTH_REDIRECT_URI: str
