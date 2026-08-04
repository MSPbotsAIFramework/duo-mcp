import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:
    @mcp.tool()
    async def duo_webauthn_credentials_retrieve_web_authn_credentials(limit: str | None = None, offset: str | None = None) -> str:
        """Retrieve WebAuthn Credentials.

        API: GET /admin/v1/webauthncredentials

        Args:
            limit: Optional. The maximum number of records returned. Default: 100; Max: 500
            offset: Optional. The offset from 0 at which to start record retrieval. When used with "limit", the handler will return "limit" records starting at the n-th record, where n is the offset. Default: 0
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"limit": limit, "offset": offset}
        try:
            result = await client.request("GET", "/admin/v1/webauthncredentials", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_webauthn_credentials_retrieve_web_authn_credentials_by_key(webauthnkey: str) -> str:
        """Retrieve WebAuthn Credentials by Key.

        API: GET /admin/v1/webauthncredentials/[webauthnkey]

        Args:
            webauthnkey: Required. Path parameter `webauthnkey`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/webauthncredentials/{webauthnkey}"
        params = {}
        try:
            result = await client.request("GET", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

