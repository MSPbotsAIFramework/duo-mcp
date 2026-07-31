import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:

    @mcp.tool()
    async def duo_trust_monitor_retrieve_events(mintime: str, maxtime: str, limit: str | None = None, offset: str | None = None, type: str | None = None) -> str:
        """Retrieve Events.

        API: GET /admin/v1/trust_monitor/events

        Args:
            mintime: Required. Return records that have a 13 character Unix timestamp in milliseconds of mintime or later. This value must be strictly less then maxtime.
            maxtime: Required. Return records that have a 13 character Unix timestamp in milliseconds of maxtime or earlier. This value must be strictly greater then mintime.
            limit: Optional. The maximum number of records returned. Default: 100; Max: 500
            offset: Optional. The offset from 0 at which to start record retrieval. When used with "limit", the handler will return "limit" records starting at the n-th record, where n is the offset. Default: 0
            type: Optional. The type of security event. auth Return security events that are denied anomalous authentications. bypass_status_enabled Return security events that are bypass status enabled.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"limit": limit, "offset": offset, "mintime": mintime, "maxtime": maxtime, "type": type}
        try:
            result = await client.request("GET", "/admin/v1/trust_monitor/events", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"
