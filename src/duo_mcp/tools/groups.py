import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:

    @mcp.tool()
    async def duo_groups_associate_group_with_user(user_id: str, group_id: str) -> str:
        """Associate Group with User.

        API: POST /admin/v1/users/{user_id}/groups

        Args:
            user_id: Required. Path parameter `user_id`.
            group_id: Required. The ID of the group to associate with the user.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/users/{user_id}/groups"
        params = {"group_id": group_id}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_groups_create_group(name: str, desc: str | None = None, status: str | None = None) -> str:
        """Create Group.

        API: POST /admin/v1/groups

        Args:
            name: Required. The name of the group.
            desc: Optional. The description of the group.
            status: Optional. The authentication status of the group. May be one of: “active” - The users in the group must complete secondary authentication. “bypass” - The users in the group will bypass secondary authentication after completing primary authentication. “disabled” - The users in the group will not be able to authenticate.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"name": name, "desc": desc, "status": status}
        try:
            result = await client.request("POST", "/admin/v1/groups", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_groups_delete_group(group_id: str) -> str:
        """Delete Group.

        API: DELETE /admin/v1/groups/{group_id}

        Args:
            group_id: Required. Path parameter `group_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/groups/{group_id}"
        params = {}
        try:
            result = await client.request("DELETE", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_groups_disassociate_group_from_user(user_id: str, group_id: str) -> str:
        """Disassociate Group from User.

        API: DELETE /admin/v1/users/{user_id}/groups/{group_id}

        Args:
            user_id: Required. Path parameter `user_id`.
            group_id: Required. Path parameter `group_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/users/{user_id}/groups/{group_id}"
        params = {}
        try:
            result = await client.request("DELETE", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

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
    async def duo_groups_get_group_members(group_id: str) -> str:
        """Get Group Members.

        API: GET /admin/v2/groups/{group_id}/users

        Args:
            group_id: Required. Path parameter `group_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v2/groups/{group_id}/users"
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

    @mcp.tool()
    async def duo_groups_retrieve_groups_by_user_id(user_id: str, limit: str | None = None, offset: str | None = None) -> str:
        """Retrieve Groups by User ID.

        API: GET /admin/v1/users/{user_id}/groups

        Args:
            user_id: Required. Path parameter `user_id`.
            limit: Optional. The maximum number of records returned. Default: 100; Max: 500
            offset: Optional. The offset from 0 at which to start record retrieval. When used with "limit", the handler will return "limit" records starting at the n-th record, where n is the offset. Default: 0
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/users/{user_id}/groups"
        params = {"limit": limit, "offset": offset}
        try:
            result = await client.request("GET", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_groups_update_group(group_id: str, name: str | None = None, desc: str | None = None, status: str | None = None) -> str:
        """Update Group.

        API: POST /admin/v1/groups/{group_id}

        Args:
            group_id: Required. Path parameter `group_id`.
            name: Optional. Update the name of the group.
            desc: Optional. Update the description of the group.
            status: Optional. The authentication status of the group. May be one of: “active” - The users in the group must complete secondary authentication. “bypass” - The users in the group will bypass secondary authentication after completing primary authentication. “disabled” - The users in the group will not be able to authenticate.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/groups/{group_id}"
        params = {"name": name, "desc": desc, "status": status}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"
