import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:

    @mcp.tool()
    async def duo_desktop_authenticators_create_shared_device_authentication_configuration(body: dict) -> str:
        """Create Shared Device Authentication Configuration.

        API: POST /admin/v1/desktop_authenticators/shared_device_auth

        Args:
            body: Required. JSON request payload sent verbatim as the signed request body. Top-level fields (from the vendor's example): `group_id_list`, `trusted_endpoint_integration_id_list`. See the Duo Admin API docs for this resource's exact schema.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = body
        try:
            result = await client.request("POST", "/admin/v1/desktop_authenticators/shared_device_auth", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_desktop_authenticators_delete_desktop_authenticator(dakey: str) -> str:
        """Delete Desktop Authenticator.

        API: DELETE /admin/v1/desktop_authenticators/{dakey}

        Args:
            dakey: Required. Path parameter `dakey`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/desktop_authenticators/{dakey}"
        params = {}
        try:
            result = await client.request("DELETE", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_desktop_authenticators_retrieve_desktop_authenticator_by_id(dakey: str) -> str:
        """Retrieve Desktop Authenticator by ID.

        API: GET /admin/v1/desktop_authenticators/{dakey}

        Args:
            dakey: Required. Path parameter `dakey`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/desktop_authenticators/{dakey}"
        params = {}
        try:
            result = await client.request("GET", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_desktop_authenticators_retrieve_desktop_authenticators(limit: str | None = None, offset: str | None = None) -> str:
        """Retrieve Desktop Authenticators.

        API: GET /admin/v1/desktop_authenticators

        Args:
            limit: Optional. The maximum number of records returned.
            offset: Optional. The offset from 0 at which to start record retrieval.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"limit": limit, "offset": offset}
        try:
            result = await client.request("GET", "/admin/v1/desktop_authenticators", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_desktop_authenticators_retrieve_shared_device_authentication_configuration_by_key(shared_device_key: str) -> str:
        """Retrieve Shared Device Authentication Configuration by Key.

        API: GET /admin/v1/desktop_authenticators/shared_device_auth/{shared_device_key}

        Args:
            shared_device_key: Required. Path parameter `shared_device_key`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/desktop_authenticators/shared_device_auth/{shared_device_key}"
        params = {}
        try:
            result = await client.request("GET", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_desktop_authenticators_retrieve_shared_device_authentication_configurations(limit: str | None = None, offset: str | None = None) -> str:
        """Retrieve Shared Device Authentication Configurations.

        API: GET /admin/v1/desktop_authenticators/shared_device_auth

        Args:
            limit: Optional. The maximum number of records returned.
            offset: Optional. The offset from 0 at which to start record retrieval.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"limit": limit, "offset": offset}
        try:
            result = await client.request("GET", "/admin/v1/desktop_authenticators/shared_device_auth", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_desktop_authenticators_update_shared_device_authentication_configuration(shared_device_key: str, body: dict) -> str:
        """Update Shared Device Authentication Configuration.

        API: PUT /admin/v1/desktop_authenticators/shared_device_auth/{shared_device_key}

        Args:
            shared_device_key: Required. Path parameter `shared_device_key`.
            body: Required. JSON request payload sent verbatim as the signed request body. Top-level fields (from the vendor's example): `active`, `group_id_list`, `name`, `trusted_endpoint_integration_id_list`. See the Duo Admin API docs for this resource's exact schema.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/desktop_authenticators/shared_device_auth/{shared_device_key}"
        params = body
        try:
            result = await client.request("PUT", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_desktop_authenticators_update_shared_device_authentication_configuration_copy(shared_device_key: str) -> str:
        """Update Shared Device Authentication Configuration Copy.

        API: DELETE /admin/v1/desktop_authenticators/shared_device_auth/{shared_device_key}

        Args:
            shared_device_key: Required. Path parameter `shared_device_key`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/desktop_authenticators/shared_device_auth/{shared_device_key}"
        params = {}
        try:
            result = await client.request("DELETE", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"
