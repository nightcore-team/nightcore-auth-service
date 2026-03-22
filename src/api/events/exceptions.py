"""Exceptions handlers for the API."""

from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.core.security.exceptions import TokenError
from src.domain.exceptions.base import AuthError
from src.domain.exceptions.session import SessionNotFoundError
from src.domain.exceptions.token import (
    RefreshTokenNotProvidedError,
    TokenRevokedError,
)
from src.infrastructure.discord.exceptions import (
    AuthorizationCodeNotProvidedError,
    DiscordAPIError,
    DiscordAuthError,
    TokenExchangeError,
    UserInfoRetrievalError,
)
from src.infrastructure.redis.exceptions import RedisError


async def auth_exception_handler(_: Request, exc: AuthError) -> JSONResponse:
    """Handle authentication errors."""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
    )


async def business_exception_handler(
    _: Request,
    exc: SessionNotFoundError
    | RefreshTokenNotProvidedError
    | TokenRevokedError,
) -> JSONResponse:
    """Handle business-related errors."""

    status_code = status.HTTP_401_UNAUTHORIZED

    if isinstance(exc, RefreshTokenNotProvidedError):
        status_code = status.HTTP_400_BAD_REQUEST

    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)},
    )


async def discord_exception_handler(
    _: Request,
    exc: DiscordAuthError
    | AuthorizationCodeNotProvidedError
    | DiscordAPIError
    | UserInfoRetrievalError
    | TokenExchangeError,
):
    """Handle Discord-related errors."""

    status_code = status.HTTP_401_UNAUTHORIZED

    if isinstance(exc, AuthorizationCodeNotProvidedError):
        status_code = status.HTTP_400_BAD_REQUEST
    elif isinstance(
        exc, DiscordAPIError | UserInfoRetrievalError | TokenExchangeError
    ):
        status_code = status.HTTP_502_BAD_GATEWAY

    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)},
    )


async def jwt_exception_handler(_: Request, exc: TokenError) -> JSONResponse:
    """Handle jwt-related errors."""

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
    )


async def storage_exception_handler(
    _: Request, exc: RedisError
) -> JSONResponse:
    """Handle storage-related errors."""

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": str(exc)},
    )


async def unexpected_exception_handler(
    _: Request, exc: Exception
) -> JSONResponse:
    """Handle unexpected errors."""

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )


EXCEPTION_HANDLERS = {
    AuthError: auth_exception_handler,
    SessionNotFoundError: business_exception_handler,
    RefreshTokenNotProvidedError: business_exception_handler,
    TokenRevokedError: business_exception_handler,
    AuthorizationCodeNotProvidedError: discord_exception_handler,
    DiscordAPIError: discord_exception_handler,
    UserInfoRetrievalError: discord_exception_handler,
    TokenExchangeError: discord_exception_handler,
    TokenError: jwt_exception_handler,
    RedisError: storage_exception_handler,
    Exception: unexpected_exception_handler,
}
