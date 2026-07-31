import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:

    @mcp.tool()
    async def duo_logs_activity_logs(mintime: str, maxtime: str, limit: str | None = None, next_offset: str | None = None, sort: str | None = None) -> str:
        """Activity Logs.

        API: GET /admin/v2/logs/activity

        Args:
            mintime: Required. Unix timestamp in milliseconds of the oldest log entries to collect
            maxtime: Required. Unix timestamp in milliseconds of newest log entry to collect. Must be greater than `mintime` value and no more than 180 days from today.
            limit: Optional. Number of log entries to return. Default is 100. Max is 1000
            next_offset: Optional. Offset to begin log retrieval. Used with paged responses when more than `limit` entries are available. This ia a comma separated string containing a timestamp and transaction ID Example: 1547486297000,5bea1c1e-612c-4f1d-b310-75fd31385b15
            sort: Optional. Order for the returned results. Options are 'ts:asc' or ts:desc' Default is 'ts:desc'
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"mintime": mintime, "maxtime": maxtime, "limit": limit, "next_offset": next_offset, "sort": sort}
        try:
            result = await client.request("GET", "/admin/v2/logs/activity", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_logs_administrator_logs(mintime: str | None = None) -> str:
        """Administrator Logs.

        API: GET /admin/v1/logs/administrator

        Args:
            mintime: Optional. Query parameter `mintime`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"mintime": mintime}
        try:
            result = await client.request("GET", "/admin/v1/logs/administrator", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_logs_authentication_logs(mintime: str, maxtime: str, limit: str | None = None, next_offset: str | None = None, sort: str | None = None, applications: str | None = None, users: str | None = None, event_types: str | None = None, factors: str | None = None, groups: str | None = None, phone_numbers: str | None = None, reasons: str | None = None, results: str | None = None, registration_id: str | None = None, token_id: str | None = None, webauthnkey: str | None = None) -> str:
        """Authentication Logs.

        API: GET /admin/v2/logs/authentication

        Args:
            mintime: Required. Defaults to the number of days defined in the "timestampDaysOffset" collection variable
            maxtime: Required. Defaults to current time
            limit: Optional. Query parameter `limit`.
            next_offset: Optional. Query parameter `next_offset`.
            sort: Optional. Query parameter `sort`.
            applications: Optional. Query parameter `applications`.
            users: Optional. Query parameter `users`.
            event_types: Optional. Query parameter `event_types`.
            factors: Optional. Query parameter `factors`.
            groups: Optional. Query parameter `groups`.
            phone_numbers: Optional. Query parameter `phone_numbers`.
            reasons: Optional. Query parameter `reasons`.
            results: Optional. Query parameter `results`.
            registration_id: Optional. Query parameter `registration_id`.
            token_id: Optional. Query parameter `token_id`.
            webauthnkey: Optional. Query parameter `webauthnkey`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"limit": limit, "next_offset": next_offset, "sort": sort, "mintime": mintime, "maxtime": maxtime, "applications": applications, "users": users, "event_types": event_types, "factors": factors, "groups": groups, "phone_numbers": phone_numbers, "reasons": reasons, "results": results, "registration_id": registration_id, "token_id": token_id, "webauthnkey": webauthnkey}
        try:
            result = await client.request("GET", "/admin/v2/logs/authentication", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_logs_authentication_logs_legacy_v1(mintime: str | None = None) -> str:
        """Authentication Logs (Legacy v1).

        API: GET /admin/v1/logs/authentication

        Args:
            mintime: Optional. Query parameter `mintime`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"mintime": mintime}
        try:
            result = await client.request("GET", "/admin/v1/logs/authentication", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_logs_offline_enrollment_logs(mintime: str | None = None) -> str:
        """Offline Enrollment Logs.

        API: GET /admin/v1/logs/offline_enrollment

        Args:
            mintime: Optional. Query parameter `mintime`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"mintime": mintime}
        try:
            result = await client.request("GET", "/admin/v1/logs/offline_enrollment", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_logs_telephony_logs(mintime: str | None = None) -> str:
        """Telephony Logs.

        API: GET /admin/v1/logs/telephony

        Args:
            mintime: Optional. Query parameter `mintime`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"mintime": mintime}
        try:
            result = await client.request("GET", "/admin/v1/logs/telephony", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_logs_telephony_logs_v2(mintime: str, maxtime: str) -> str:
        """Telephony Logs (v2).

        API: GET /admin/v2/logs/telephony

        Args:
            mintime: Required. . Unix timestamp in milliseconds.
            maxtime: Required. . Unix timestamp in milliseconds.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"mintime": mintime, "maxtime": maxtime}
        try:
            result = await client.request("GET", "/admin/v2/logs/telephony", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"
