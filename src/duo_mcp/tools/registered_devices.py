import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:

    @mcp.tool()
    async def duo_registered_devices_block_device_by_id(compkey: str) -> str:
        """Block Device by ID.

        API: POST /admin/v1/registered_devices/blocked/{compkey}

        Args:
            compkey: Required. Path parameter `compkey`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/registered_devices/blocked/{compkey}"
        params = {}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_registered_devices_block_devices(body: dict) -> str:
        """Block Devices.

        API: POST /admin/v1/registered_devices/blocked

        Args:
            body: Required. JSON request payload sent verbatim as the signed request body. Top-level fields (from the vendor's example): `registered_device_key_list`. See the Duo Admin API docs for this resource's exact schema.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = body
        try:
            result = await client.request("POST", "/admin/v1/registered_devices/blocked", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_registered_devices_delete_registered_device(registered_device_key: str) -> str:
        """Delete Registered Device.

        API: DELETE /admin/v1/registered_devices/{registered_device_key}

        Args:
            registered_device_key: Required. Path parameter `registered_device_key`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/registered_devices/{registered_device_key}"
        params = {}
        try:
            result = await client.request("DELETE", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_registered_devices_retrieve_blocked_devices() -> str:
        """Retrieve Blocked Devices.

        API: GET /admin/v1/registered_devices/blocked

        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.request("GET", "/admin/v1/registered_devices/blocked", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_registered_devices_retrieve_blocked_devices_by_id(compkey: str) -> str:
        """Retrieve Blocked Devices by ID.

        API: GET /admin/v1/registered_devices/blocked/{compkey}

        Args:
            compkey: Required. Path parameter `compkey`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/registered_devices/blocked/{compkey}"
        params = {}
        try:
            result = await client.request("GET", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_registered_devices_retrieve_registered_device_by_id(registered_device_key: str) -> str:
        """Retrieve Registered Device by ID.

        API: GET /admin/v1/registered_devices/{registered_device_key}

        Args:
            registered_device_key: Required. Path parameter `registered_device_key`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/registered_devices/{registered_device_key}"
        params = {}
        try:
            result = await client.request("GET", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_registered_devices_retrieve_registered_devices() -> str:
        """Retrieve Registered Devices.

        API: GET /admin/v1/registered_devices

        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.request("GET", "/admin/v1/registered_devices", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_registered_devices_unblock_device_by_id(compkey: str) -> str:
        """Unblock Device by ID.

        API: DELETE /admin/v1/registered_devices/blocked/{compkey}

        Args:
            compkey: Required. Path parameter `compkey`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/registered_devices/blocked/{compkey}"
        params = {}
        try:
            result = await client.request("DELETE", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_registered_devices_unblock_devices(body: dict) -> str:
        """Unblock Devices.

        API: DELETE /admin/v1/registered_devices/blocked

        Args:
            body: Required. JSON request payload sent verbatim as the signed request body. Top-level fields (from the vendor's example): `registered_device_key_list`. See the Duo Admin API docs for this resource's exact schema.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = body
        try:
            result = await client.request("DELETE", "/admin/v1/registered_devices/blocked", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"
