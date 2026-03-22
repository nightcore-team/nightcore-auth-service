"""Interface for base external API services."""

from typing import Any, Protocol


class IOAuthProvider(Protocol):
    def get_authorization_url(self) -> str:
        """Get the URL to redirect the user to for authorization."""
        ...

    async def exchange_code(self, code: str | None) -> Any:
        """Exchange the authorization code for an access token."""
        ...

    async def get_user_info(self, token_data: Any) -> Any:
        """Get the user's information using the access token."""
        ...

    async def refresh_token(self, refresh_token: str) -> Any:
        """Refresh the access token using the refresh token."""
        ...
