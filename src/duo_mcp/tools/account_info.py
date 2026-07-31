import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:

    @mcp.tool()
    async def duo_account_info_authentication_attempts_report(maxtime: str | None = None, mintime: str | None = None) -> str:
        """Authentication Attempts Report.

        API: GET /admin/v1/info/authentication_attempts

        Args:
            maxtime: Optional. Limit report to events before this UNIX timestamp. Defaults to the current time.
            mintime: Optional. Limit report to events after this UNIX timestamp. Defaults to thirty days before maxtime.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"maxtime": maxtime, "mintime": mintime}
        try:
            result = await client.request("GET", "/admin/v1/info/authentication_attempts", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_account_info_retrieve_summary(username: str | None = None, limit: str | None = None, offset: str | None = None) -> str:
        """Retrieve Summary.

        API: GET /admin/v1/users

        Args:
            username: Optional. Specify a user name (or username alias) to look up a single user.
            limit: Optional. The maximum number of records returned. Default: 100; Max: 300
            offset: Optional. The offset from 0 at which to start record retrieval. When used with "limit", the handler will return "limit" records starting at the n-th record, where n is the offset. Default: 0
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"username": username, "limit": limit, "offset": offset}
        try:
            result = await client.request("GET", "/admin/v1/users", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_account_info_telephony_credits_used_report_copy(username: str | None = None, limit: str | None = None, offset: str | None = None) -> str:
        """Telephony Credits Used Report Copy.

        API: GET /admin/v1/users

        Args:
            username: Optional. Specify a user name (or username alias) to look up a single user.
            limit: Optional. The maximum number of records returned. Default: 100; Max: 300
            offset: Optional. The offset from 0 at which to start record retrieval. When used with "limit", the handler will return "limit" records starting at the n-th record, where n is the offset. Default: 0
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"username": username, "limit": limit, "offset": offset}
        try:
            result = await client.request("GET", "/admin/v1/users", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_account_info_users_with_authentication_attempts_report(maxtime: str | None = None, mintime: str | None = None) -> str:
        """Users with Authentication Attempts Report.

        API: GET /admin/v1/info/user_authentication_attempts

        Args:
            maxtime: Optional. Limit report to events before this UNIX timestamp. Defaults to the current time.
            mintime: Optional. Limit report to events after this UNIX timestamp. Defaults to thirty days before maxtime.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"maxtime": maxtime, "mintime": mintime}
        try:
            result = await client.request("GET", "/admin/v1/info/user_authentication_attempts", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"
