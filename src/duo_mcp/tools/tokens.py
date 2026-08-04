import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:
    @mcp.tool()
    async def duo_tokens_retrieve_hardware_token_by_id(token_id: str) -> str:
        """Retrieve Hardware Token by ID.

        API: GET /admin/v1/tokens/{token_id}

        Args:
            token_id: Required. Path parameter `token_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/tokens/{token_id}"
        params = {}
        try:
            result = await client.request("GET", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_tokens_retrieve_hardware_tokens(type: str | None = None, serial: str | None = None, limit: str | None = None, offset: str | None = None) -> str:
        """Retrieve Hardware Tokens.

        API: GET /admin/v1/tokens

        Args:
            type: Optional. Specify a type and serial number to look up a single hardware token. One of: “h6” - HOTP-6 hardware token “h8” - HOTP-8 hardware token “yk” - YubiKey AES hardware token “d1” - Duo-D100 hardware token f * This option is required if serial is present.
            serial: Optional. The serial number of the hardware token. * This option is required if type is present.
            limit: Optional. The maximum number of records returned. Default: 100; Max: 500
            offset: Optional. The offset from 0 at which to start record retrieval. When used with "limit", the handler will return "limit" records starting at the n-th record, where n is the offset. Default: 0
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"type": type, "serial": serial, "limit": limit, "offset": offset}
        try:
            result = await client.request("GET", "/admin/v1/tokens", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"
