import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:

    @mcp.tool()
    async def duo_tokens_create_hardware_token(type: str, serial: str, secret: str | None = None, counter: str | None = None, private_id: str | None = None, aes_key: str | None = None) -> str:
        """Create Hardware Token.

        API: POST /admin/v1/tokens

        Args:
            type: Required. The type of hardware token to import. One of: “h6” - HOTP-6 hardware token “h8” - HOTP-8 hardware token “yk” - YubiKey AES hardware token Duo-D100 tokens (type "d1") are imported when purchased from Duo and may not be created via the Admin API.
            serial: Required. The serial number of the token (maximum length 128 characters).
            secret: Optional. The HOTP secret. This parameter is required for HOTP-6 and HOTP-8 hardware tokens.
            counter: Optional. Initial value for the HOTP counter. Default: 0. This parameter is only valid for HOTP-6 and HOTP-8 hardware tokens.
            private_id: Optional. The YubiKey private ID. This parameter is required for YubiKey hardware tokens.
            aes_key: Optional. The YubiKey AES key. This parameter is required for YubiKey hardware tokens.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"type": type, "serial": serial, "secret": secret, "counter": counter, "private_id": private_id, "aes_key": aes_key}
        try:
            result = await client.request("POST", "/admin/v1/tokens", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_tokens_delete_hardware_token(token_id: str) -> str:
        """Delete Hardware Token.

        API: DELETE /admin/v1/tokens/{token_id}

        Args:
            token_id: Required. Path parameter `token_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/tokens/{token_id}"
        params = {}
        try:
            result = await client.request("DELETE", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_tokens_resync_hardware_token(token_id: str, code1: str, code2: str, code3: str) -> str:
        """Resync Hardware Token.

        API: POST /admin/v1/tokens/{token_id}/resync

        Args:
            token_id: Required. Path parameter `token_id`.
            code1: Required. The first code from the token.
            code2: Required. The second code from the token.
            code3: Required. The third code from the token.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/tokens/{token_id}/resync"
        params = {"code1": code1, "code2": code2, "code3": code3}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

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
