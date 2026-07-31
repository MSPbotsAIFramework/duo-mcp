import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:

    @mcp.tool()
    async def duo_endpoints_retrieve_endpoints(limit: str | None = None, offset: str | None = None) -> str:
        """Retrieve Endpoints.

        API: GET /admin/v1/endpoints

        Args:
            limit: Optional. Query parameter `limit`.
            offset: Optional. Query parameter `offset`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"limit": limit, "offset": offset}
        try:
            result = await client.request("GET", "/admin/v1/endpoints", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_endpoints_retrieve_endpoints_by_id(epkey: str) -> str:
        """Retrieve Endpoints by ID.

        API: GET /admin/v1/endpoints/[epkey]

        Args:
            epkey: Required. Path parameter `epkey`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/endpoints/{epkey}"
        params = {}
        try:
            result = await client.request("GET", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"
