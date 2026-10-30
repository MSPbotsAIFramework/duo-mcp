from collections.abc import Callable
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .._json import dump_json_capped
from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:
    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def duo_logs_administrator_logs(
        mintime: Annotated[
            str | None,
            Field(
                description=(
                    "Unix timestamp in seconds; only return entries at or after "
                    "this time (default: all)."
                )
            ),
        ] = None,
    ) -> str:
        """List administrator activity log entries (who did what, and when)."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"mintime": mintime}
        try:
            result = await client.request("GET", "/admin/v1/logs/administrator", params=params)
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()
