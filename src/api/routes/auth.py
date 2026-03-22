"""Authentication endpoints."""

from fastapi import APIRouter, Request, Response, status
from fastapi.responses import RedirectResponse

from src.api.dependencies import OICServiceDependency
from src.api.schemas import Token as TokenResponse

router = APIRouter()


@router.post(
    "/refresh", status_code=status.HTTP_200_OK, response_model=TokenResponse
)
async def refresh(
    request: Request, response: Response, service: OICServiceDependency
):
    """Refresh access token by refresh token."""
    refresh_token = request.cookies.get("refresh_token")
    ip_address = request.client.host if request.client else "unknown"

    token = await service.refresh(
        refresh_token=refresh_token, ip_address=ip_address
    )

    response.set_cookie(
        "refresh_token",
        token.refresh_token,
        httponly=True,
        max_age=service.config.jwt.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
    )

    return TokenResponse(access_token=token.access_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request, response: Response, service: OICServiceDependency
) -> None:
    """Logout user by refresh token."""

    refresh_token = request.cookies.get("refresh_token")

    response.delete_cookie("refresh_token", httponly=True)

    await service.logout(refresh_token=refresh_token)


@router.post("/discord", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def discord(service: OICServiceDependency) -> RedirectResponse:
    """Authenticate user by Discord."""

    return RedirectResponse(url=service.oauth_provider.get_authorization_url())


@router.get(
    "/discord/callback",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
)
async def discord_callback(
    code: str,
    request: Request,
    response: Response,
    service: OICServiceDependency,
):
    """Handle Discord auth callback."""
    ip_address = request.client.host if request.client else "unknown"

    token = await service.login(code=code, ip_address=ip_address)

    response.set_cookie(
        "refresh_token",
        token.refresh_token,
        httponly=True,
        max_age=service.config.jwt.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
    )

    return TokenResponse(access_token=token.access_token)
