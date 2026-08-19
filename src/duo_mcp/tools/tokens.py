from collections.abc import Callable
from typing import Annotated, Literal

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .._json import dump_json_capped
from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN

# Duo's documented hard cap for GET /admin/v1/tokens (duo.com/docs/adminapi).
_MAX_LIMIT = 500


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:
    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def duo_tokens_retrieve_hardware_token_by_id(
        token_id: Annotated[str, Field(description="Hardware token ID to look up.")],
    ) -> str:
        """Get a single hardware token's details by ID."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/tokens/{token_id}"
        try:
            result = await client.request("GET", path, params={})
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def duo_tokens_retrieve_hardware_tokens(
        type: Annotated[
            Literal["h6", "h8", "yk", "d1"] | None,
            Field(description="Hardware token type filter. Requires serial."),
        ] = None,
        serial: Annotated[
            str | None, Field(description="Token serial number. Requires type.")
        ] = None,
        limit: Annotated[
            int | None, Field(description="Max records to return (default 100, max 500).")
        ] = None,
        offset: Annotated[
            int | None, Field(description="Offset from 0 to start record retrieval.")
        ] = None,
    ) -> str:
        """List hardware tokens in the account."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        if limit is not None:
            limit = min(limit, _MAX_LIMIT)
        params = {"type": type, "serial": serial, "limit": limit, "offset": offset}
        try:
            result = await client.request("GET", "/admin/v1/tokens", params=params)
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()
