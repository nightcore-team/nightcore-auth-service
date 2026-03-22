"""Discord OAuth provider implementation."""

import aiohttp

from src.domain.interfaces.oauth_provider import IOAuthProvider
from src.infrastructure.discord.entities import DiscordTokenData, DiscordUser

from .config import Config as DiscordConfig
from .exceptions import (
    AuthorizationCodeNotProvidedError,
    DiscordAPIError,
    TokenExchangeError,
    UserInfoRetrievalError,
)


class DiscordOAuthProvider(IOAuthProvider):
    def __init__(self, config: DiscordConfig):
        self.config = config

    def get_authorization_url(self):
        """Get the URL to redirect the user to for authorization."""

        return (
            f"https://discord.com/oauth2/authorize"
            f"?client_id={self.config.DISCORD_AUTH_CLIENT_ID}"
            f"&redirect_uri={self.config.DISCORD_AUTH_REDIRECT_URI}"
            f"&response_type=code&scope=identify"
        )

    async def exchange_code(self, code: str | None) -> DiscordTokenData:
        """Exchange the authorization code for an access token."""

        if not code:
            raise AuthorizationCodeNotProvidedError(
                "Authorization code not provided in the callback"
            )

        try:
            async with (
                aiohttp.ClientSession() as session,
                session.post(
                    "https://discord.com/api/oauth2/token",
                    data={
                        "client_id": self.config.DISCORD_AUTH_CLIENT_ID,
                        "client_secret": self.config.DISCORD_AUTH_CLIENT_SECRET,  # noqa: E501
                        "grant_type": "authorization_code",
                        "code": code,
                        "redirect_uri": self.config.DISCORD_AUTH_REDIRECT_URI,
                    },
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                ) as response,
            ):
                data = await response.json()

                if response.status != 200:
                    raise TokenExchangeError(
                        f"Discord API error ({response.status}): {data}"
                    )

                try:
                    return DiscordTokenData(**data)
                except TypeError as e:
                    raise TokenExchangeError(
                        "Invalid token data received from Discord"
                    ) from e

        except aiohttp.ClientError as e:
            raise DiscordAPIError(
                "Failed to communicate with Discord API"
            ) from e

    async def get_user_info(self, token_data: DiscordTokenData) -> DiscordUser:
        """Get the user's information using the access token."""

        access_token = token_data.access_token

        try:
            async with (
                aiohttp.ClientSession() as session,
                session.get(
                    "https://discord.com/api/users/@me",
                    headers={"Authorization": f"Bearer {access_token}"},
                ) as response,
            ):
                data = await response.json()

                if response.status != 200:
                    raise UserInfoRetrievalError(
                        f"Discord API error ({response.status}): {data}"
                    )

                try:
                    return DiscordUser(id=data.get("id"))
                except TypeError as e:
                    raise UserInfoRetrievalError(
                        "Invalid user data received from Discord"
                    ) from e

        except aiohttp.ClientError as e:
            raise DiscordAPIError(
                "Failed to communicate with Discord API"
            ) from e
