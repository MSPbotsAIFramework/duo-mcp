import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:
    @mcp.tool()
    async def duo_groups_get_group_info(group_id: str) -> str:
        """Get Group Info.

        API: GET /admin/v2/groups/{group_id}

        Args:
            group_id: Required. Path parameter `group_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v2/groups/{group_id}"
        params = {}
        try:
            result = await client.request("GET", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_groups_retrieve_groups(limit: str | None = None, offset: str | None = None) -> str:
        """Retrieve Groups.

        API: GET /admin/v1/groups

        Args:
            limit: Optional. The maximum number of records returned. Default: 100; Max: 500
            offset: Optional. The offset from 0 at which to start record retrieval. When used with "limit", the handler will return "limit" records starting at the n-th record, where n is the offset. Default: 0
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"limit": limit, "offset": offset}
        try:
            result = await client.request("GET", "/admin/v1/groups", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

