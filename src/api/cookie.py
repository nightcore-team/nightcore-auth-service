"""Cookie helpers."""

from typing import TYPE_CHECKING

from fastapi import Response

if TYPE_CHECKING:
    from src.core.config._global import Config


def _get_samesite(config: "Config"):
    samesite = "lax"
    if config.env.ENVIRONMENT == "test":
        samesite = "none"

    return samesite


def set_cookie(config: "Config", response: Response, value: str) -> None:
    """Set the refresh token cookie on the response."""

    samesite = _get_samesite(config)

    response.set_cookie(
        config.api.REFRESH_TOKEN_COOKIE_NAME,
        value,
        httponly=True,
        max_age=config.jwt.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
        samesite=samesite,
        secure=True,
    )


def delete_cookie(config: "Config", response: Response) -> None:
    """Delete the refresh token cookie from the response."""

    samesite = _get_samesite(config)

    response.delete_cookie(
        config.api.REFRESH_TOKEN_COOKIE_NAME,
        httponly=True,
        samesite=samesite,
        secure=True,
    )
