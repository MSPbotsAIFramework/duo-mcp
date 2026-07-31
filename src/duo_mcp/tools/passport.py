import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:

    @mcp.tool()
    async def duo_passport_get_configuration() -> str:
        """Get Configuration.

        API: GET /admin/v2/passport/config

        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.request("GET", "/admin/v2/passport/config", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_passport_modify_configuration(body: dict) -> str:
        """Modify Configuration.

        API: POST /admin/v2/passport/config

        Args:
            body: Required. JSON request payload sent verbatim as the signed request body. Top-level fields (from the vendor's example): `disabled_groups`, `enabled_groups`, `enabled_status`. See the Duo Admin API docs for this resource's exact schema.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = body
        try:
            result = await client.request("POST", "/admin/v2/passport/config", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"
