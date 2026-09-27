"""API configuration."""

from src.core.config.env import BaseEnvConfig


class Config(BaseEnvConfig):
    """Configuration class for the API."""

    API_HOST: str
    API_PORT: int
    REFRESH_TOKEN_COOKIE_NAME: str = "refresh_token"
    DASHBOARD_FRONTEND_URI: str
