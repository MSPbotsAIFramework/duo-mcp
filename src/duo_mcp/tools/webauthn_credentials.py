from collections.abc import Callable
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .._json import dump_json_capped
from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN

# Duo's documented hard cap for GET /admin/v1/webauthncredentials
# (duo.com/docs/adminapi; extracted from Duo's own Postman collection).
_MAX_LIMIT = 500


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:
    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def duo_webauthn_credentials_retrieve_web_authn_credentials(
        limit: Annotated[
            int | None, Field(description="Max records to return (default 100, max 500).")
        ] = None,
        offset: Annotated[
            int | None, Field(description="Offset from 0 to start record retrieval.")
        ] = None,
    ) -> str:
        """List WebAuthn (security key) credentials in the account."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        if limit is not None:
            limit = min(limit, _MAX_LIMIT)
        params = {"limit": limit, "offset": offset}
        try:
            result = await client.request(
                "GET", "/admin/v1/webauthncredentials", params=params
            )
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def duo_webauthn_credentials_retrieve_web_authn_credentials_by_key(
        webauthnkey: Annotated[str, Field(description="WebAuthn credential key to look up.")],
    ) -> str:
        """Get a single WebAuthn credential's details by key."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/webauthncredentials/{webauthnkey}"
        try:
            result = await client.request("GET", path, params={})
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()
