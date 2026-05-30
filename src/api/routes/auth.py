"""Authentication endpoints."""

from fastapi import APIRouter, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse

from src.api.dependencies import AppConfigDependency, OICServiceDependency
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


@router.get("/login", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def login(service: OICServiceDependency) -> RedirectResponse:
    """Authenticate user by Discord."""

    return RedirectResponse(url=service.oauth_provider.get_authorization_url())


@router.get(
    "/discord/callback",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
)
async def discord_callback(
    code: str | None,
    error: str | None,
    request: Request,
    service: OICServiceDependency,
    config: AppConfigDependency,
):
    """Handle Discord auth callback."""

    if error is not None:
        return RedirectResponse(
            url=config.api.DASHBOARD_FRONTEND_URI,
            status_code=status.HTTP_302_FOUND,
        )

    if code is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code is not found in query",
        )

    ip_address = request.client.host if request.client else "unknown"

    token = await service.login(code=code, ip_address=ip_address)

    response = RedirectResponse(
        url=config.api.DASHBOARD_FRONTEND_URI,
        status_code=status.HTTP_302_FOUND,
    )

    response.set_cookie(
        "refresh_token",
        token.refresh_token,
        httponly=True,
        max_age=service.config.jwt.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
    )

    return response
