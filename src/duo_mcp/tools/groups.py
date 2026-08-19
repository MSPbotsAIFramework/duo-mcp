from collections.abc import Callable
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .._json import dump_json_capped
from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN

# Duo's documented hard cap for GET /admin/v1/groups (duo.com/docs/adminapi).
_MAX_LIMIT = 500


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:
    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def duo_groups_get_group_info(
        group_id: Annotated[str, Field(description="Group ID to look up.")],
    ) -> str:
        """Get a single group's details by ID."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v2/groups/{group_id}"
        try:
            result = await client.request("GET", path, params={})
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def duo_groups_retrieve_groups(
        limit: Annotated[
            int | None, Field(description="Max records to return (default 100, max 500).")
        ] = None,
        offset: Annotated[
            int | None, Field(description="Offset from 0 to start record retrieval.")
        ] = None,
    ) -> str:
        """List groups in the account."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        if limit is not None:
            limit = min(limit, _MAX_LIMIT)
        params = {"limit": limit, "offset": offset}
        try:
            result = await client.request("GET", "/admin/v1/groups", params=params)
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()
