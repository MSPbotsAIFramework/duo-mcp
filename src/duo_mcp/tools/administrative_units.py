import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:

    @mcp.tool()
    async def duo_administrative_units_add_administrative_unit(name: str, description: str, restrict_by_groups: str | None = None, restrict_by_integrations: str | None = None, admins: str | None = None, groups: str | None = None, integrations: str | None = None) -> str:
        """Add Administrative Unit.

        API: POST /admin/v1/administrative_units

        Args:
            name: Required. Query parameter `name`.
            description: Required. Query parameter `description`.
            restrict_by_groups: Optional. Query parameter `restrict_by_groups`.
            restrict_by_integrations: Optional. Query parameter `restrict_by_integrations`.
            admins: Optional. Query parameter `admins`.
            groups: Optional. Query parameter `groups`.
            integrations: Optional. Query parameter `integrations`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"name": name, "description": description, "restrict_by_groups": restrict_by_groups, "restrict_by_integrations": restrict_by_integrations, "admins": admins, "groups": groups, "integrations": integrations}
        try:
            result = await client.request("POST", "/admin/v1/administrative_units", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrative_units_add_administrator_to_administrative_unit(admin_unit_id: str, admin_id: str) -> str:
        """Add Administrator to Administrative Unit.

        API: POST /admin/v1/administrative_units/[admin_unit_id]/admin/[admin_id]

        Args:
            admin_unit_id: Required. Path parameter `admin_unit_id`.
            admin_id: Required. Path parameter `admin_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/administrative_units/{admin_unit_id}/admin/{admin_id}"
        params = {}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrative_units_add_group_to_administrative_unit(admin_unit_id: str, goup_id: str) -> str:
        """Add Group to Administrative Unit.

        API: POST /admin/v1/administrative_units/[admin_unit_id]/group/[goup_id]

        Args:
            admin_unit_id: Required. Path parameter `admin_unit_id`.
            goup_id: Required. Path parameter `goup_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/administrative_units/{admin_unit_id}/group/{goup_id}"
        params = {}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrative_units_add_integration_to_administrative_unit(admin_unit_id: str, integration_key: str) -> str:
        """Add Integration to Administrative Unit.

        API: POST /admin/v1/administrative_units/[admin_unit_id]/integration/[integration_key]

        Args:
            admin_unit_id: Required. Path parameter `admin_unit_id`.
            integration_key: Required. Path parameter `integration_key`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/administrative_units/{admin_unit_id}/integration/{integration_key}"
        params = {}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrative_units_delete_administrative_unit(admin_unit_id: str) -> str:
        """Delete Administrative Unit.

        API: DELETE /admin/v1/administrative_units/[admin_unit_id]

        Args:
            admin_unit_id: Required. Path parameter `admin_unit_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/administrative_units/{admin_unit_id}"
        params = {}
        try:
            result = await client.request("DELETE", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrative_units_modify_administrative_unit(admin_unit_id: str, name: str | None = None, description: str | None = None, restrict_by_groups: str | None = None, restrict_by_integrations: str | None = None, admins: str | None = None, groups: str | None = None, integrations: str | None = None) -> str:
        """Modify Administrative Unit.

        API: POST /admin/v1/administrative_units/[admin_unit_id]

        Args:
            admin_unit_id: Required. Path parameter `admin_unit_id`.
            name: Optional. Query parameter `name`.
            description: Optional. Query parameter `description`.
            restrict_by_groups: Optional. Query parameter `restrict_by_groups`.
            restrict_by_integrations: Optional. Query parameter `restrict_by_integrations`.
            admins: Optional. Query parameter `admins`.
            groups: Optional. Query parameter `groups`.
            integrations: Optional. Query parameter `integrations`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/administrative_units/{admin_unit_id}"
        params = {"name": name, "description": description, "restrict_by_groups": restrict_by_groups, "restrict_by_integrations": restrict_by_integrations, "admins": admins, "groups": groups, "integrations": integrations}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrative_units_remove_administrator_from_administrative_unit(admin_unit_id: str, admin_id: str) -> str:
        """Remove Administrator from Administrative Unit.

        API: DELETE /admin/v1/administrative_units/[admin_unit_id]/admin/[admin_id]

        Args:
            admin_unit_id: Required. Path parameter `admin_unit_id`.
            admin_id: Required. Path parameter `admin_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/administrative_units/{admin_unit_id}/admin/{admin_id}"
        params = {}
        try:
            result = await client.request("DELETE", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrative_units_remove_group_from_administrative_unit(admin_unit_id: str, goup_id: str) -> str:
        """Remove Group from Administrative Unit.

        API: DELETE /admin/v1/administrative_units/[admin_unit_id]/group/[goup_id]

        Args:
            admin_unit_id: Required. Path parameter `admin_unit_id`.
            goup_id: Required. Path parameter `goup_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/administrative_units/{admin_unit_id}/group/{goup_id}"
        params = {}
        try:
            result = await client.request("DELETE", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrative_units_remove_integration_from_administrative_unit(admin_unit_id: str, integration_key: str) -> str:
        """Remove Integration from Administrative Unit.

        API: DELETE /admin/v1/administrative_units/[admin_unit_id]/integration/[integration_key]

        Args:
            admin_unit_id: Required. Path parameter `admin_unit_id`.
            integration_key: Required. Path parameter `integration_key`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/administrative_units/{admin_unit_id}/integration/{integration_key}"
        params = {}
        try:
            result = await client.request("DELETE", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrative_units_retrieve_administrative_unit_details(admin_unit_id: str) -> str:
        """Retrieve Administrative Unit Details.

        API: GET /admin/v1/administrative_units/[admin_unit_id]

        Args:
            admin_unit_id: Required. Path parameter `admin_unit_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/administrative_units/{admin_unit_id}"
        params = {}
        try:
            result = await client.request("GET", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrative_units_retrieve_administrative_units(admin_id: str | None = None, group_id: str | None = None, integration_key: str | None = None, limit: str | None = None, offset: str | None = None) -> str:
        """Retrieve Administrative Units.

        API: GET /admin/v1/administrative_units

        Args:
            admin_id: Optional. Query parameter `admin_id`.
            group_id: Optional. Query parameter `group_id`.
            integration_key: Optional. Query parameter `integration_key`.
            limit: Optional. Query parameter `limit`.
            offset: Optional. Query parameter `offset`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"admin_id": admin_id, "group_id": group_id, "integration_key": integration_key, "limit": limit, "offset": offset}
        try:
            result = await client.request("GET", "/admin/v1/administrative_units", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"
