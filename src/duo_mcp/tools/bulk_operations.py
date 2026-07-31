import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:

    @mcp.tool()
    async def duo_bulk_operations_bulk_user_operations(body: dict) -> str:
        """Bulk User Operations.

        API: POST /admin/v1/bulk

        Args:
            body: Required. JSON request payload sent verbatim as the signed request body. Top-level fields (from the vendor's example): `operations`. See the Duo Admin API docs for this resource's exact schema.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = body
        try:
            result = await client.request("POST", "/admin/v1/bulk", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"
