import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:

    @mcp.tool()
    async def duo_policies_add_new_policy_post(body: dict) -> str:
        """Add new policy.

        API: POST /admin/v2/policies

        Args:
            body: Required. JSON request payload sent verbatim as the signed request body. Top-level fields (from the vendor's example): `policy_name`. See the Duo Admin API docs for this resource's exact schema.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = body
        try:
            result = await client.request("POST", "/admin/v2/policies", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_policies_add_new_policy_post_policies(body: dict) -> str:
        """Add new policy.

        API: POST /admin/v2/policies

        Args:
            body: Required. JSON request payload sent verbatim as the signed request body. Top-level fields (from the vendor's example): `policy_name`. See the Duo Admin API docs for this resource's exact schema.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = body
        try:
            result = await client.request("POST", "/admin/v2/policies", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_policies_copy_policy(body: dict) -> str:
        """Copy Policy.

        API: POST /admin/v2/policies/copy

        Args:
            body: Required. JSON request payload sent verbatim as the signed request body. Top-level fields (from the vendor's example): `policy_key`, `new_policy_names_list`. See the Duo Admin API docs for this resource's exact schema.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = body
        try:
            result = await client.request("POST", "/admin/v2/policies/copy", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_policies_delete_policy(policy_key: str) -> str:
        """Delete policy.

        API: DELETE /admin/v2/policies/{policy_key}

        Args:
            policy_key: Required. Path parameter `policy_key`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v2/policies/{policy_key}"
        params = {}
        try:
            result = await client.request("DELETE", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_policies_get_all_policies() -> str:
        """Get all policies.

        API: GET /admin/v2/policies

        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.request("GET", "/admin/v2/policies", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_policies_get_policy_by_id(policy_key: str) -> str:
        """Get policy by ID.

        API: GET /admin/v2/policies/{policy_key}

        Args:
            policy_key: Required. Path parameter `policy_key`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v2/policies/{policy_key}"
        params = {}
        try:
            result = await client.request("GET", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_policies_resulting_policy(user_id: str, integration_key: str) -> str:
        """Resulting policy.

        API: GET /admin/v2/policies/calculate

        Args:
            user_id: Required. } The user_id of the user to evaluate, as obtained from the Retrieve Users Admin API endpoint or from the Duo Admin Panel.
            integration_key: Required. The integration_key of the application to evaluate, as obtained from the Retrieve Integrations Admin API endpoint or from the Duo Admin Panel.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"user_id": user_id, "integration_key": integration_key}
        try:
            result = await client.request("GET", "/admin/v2/policies/calculate", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_policies_summarize_policies() -> str:
        """Summarize Policies.

        API: GET /admin/v2/policies/summary

        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.request("GET", "/admin/v2/policies/summary", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_policies_update_policy(policy_key: str, body: dict) -> str:
        """Update policy.

        API: PUT /admin/v2/policies/{policy_key}

        Args:
            policy_key: Required. Path parameter `policy_key`.
            body: Required. JSON request payload sent verbatim as the signed request body. Top-level fields (from the vendor's example): `apply_to_apps`, `apply_to_groups_in_apps`. See the Duo Admin API docs for this resource's exact schema.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v2/policies/{policy_key}"
        params = body
        try:
            result = await client.request("PUT", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_policies_update_policy_deny_new_users(policy_key: str, body: dict) -> str:
        """Update policy deny new users.

        API: PUT /admin/v2/policies/{policy_key}

        Args:
            policy_key: Required. Path parameter `policy_key`.
            body: Required. JSON request payload sent verbatim as the signed request body. Top-level fields (from the vendor's example): `sections`. See the Duo Admin API docs for this resource's exact schema.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v2/policies/{policy_key}"
        params = body
        try:
            result = await client.request("PUT", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"
