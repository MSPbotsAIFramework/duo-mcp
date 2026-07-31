import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:

    @mcp.tool()
    async def duo_integrations_create_integration_v3(body: dict) -> str:
        """Create Integration (v3).

        API: POST /admin/v3/integrations

        Args:
            body: Required. JSON request payload sent verbatim as the signed request body. Top-level fields (from the vendor's example): `name`, `type`, `groups_allowed`, `user_access`. See the Duo Admin API docs for this resource's exact schema.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = body
        try:
            result = await client.request("POST", "/admin/v3/integrations", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_integrations_create_integrations_legacy(name: str, type: str, adminapi_admins: str | None = None, adminapi_info: str | None = None, adminapi_integrations: str | None = None, adminapi_read_log: str | None = None, adminapi_read_resource: str | None = None, adminapi_settings: str | None = None, adminapi_write_resource: str | None = None, enroll_policy: str | None = None, greeting: str | None = None, groups_allowed: str | None = None, ip_whitelist: str | None = None, networks_for_api_access: str | None = None, notes: str | None = None, trusted_device_days: str | None = None, self_service_allowed: str | None = None, username_normalization_policy: str | None = None) -> str:
        """Create Integrations (legacy).

        API: POST /admin/v1/integrations

        Args:
            name: Required. Query parameter `name`.
            type: Required. Query parameter `type`.
            adminapi_admins: Optional. Query parameter `adminapi_admins`.
            adminapi_info: Optional. Query parameter `adminapi_info`.
            adminapi_integrations: Optional. Query parameter `adminapi_integrations`.
            adminapi_read_log: Optional. Query parameter `adminapi_read_log`.
            adminapi_read_resource: Optional. Query parameter `adminapi_read_resource`.
            adminapi_settings: Optional. Query parameter `adminapi_settings`.
            adminapi_write_resource: Optional. Query parameter `adminapi_write_resource`.
            enroll_policy: Optional. Query parameter `enroll_policy`.
            greeting: Optional. Query parameter `greeting`.
            groups_allowed: Optional. Query parameter `groups_allowed`.
            ip_whitelist: Optional. Query parameter `ip_whitelist`.
            networks_for_api_access: Optional. Query parameter `networks_for_api_access`.
            notes: Optional. Query parameter `notes`.
            trusted_device_days: Optional. Query parameter `trusted_device_days`.
            self_service_allowed: Optional. Query parameter `self_service_allowed`.
            username_normalization_policy: Optional. Query parameter `username_normalization_policy`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"name": name, "type": type, "adminapi_admins": adminapi_admins, "adminapi_info": adminapi_info, "adminapi_integrations": adminapi_integrations, "adminapi_read_log": adminapi_read_log, "adminapi_read_resource": adminapi_read_resource, "adminapi_settings": adminapi_settings, "adminapi_write_resource": adminapi_write_resource, "enroll_policy": enroll_policy, "greeting": greeting, "groups_allowed": groups_allowed, "ip_whitelist": ip_whitelist, "networks_for_api_access": networks_for_api_access, "notes": notes, "trusted_device_days": trusted_device_days, "self_service_allowed": self_service_allowed, "username_normalization_policy": username_normalization_policy}
        try:
            result = await client.request("POST", "/admin/v1/integrations", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_integrations_create_sso_integration(body: dict) -> str:
        """Create SSO Integration.

        API: POST /admin/v2/integrations

        Args:
            body: Required. JSON request payload sent verbatim as the signed request body. Top-level fields (from the vendor's example): `name`, `type`, `sso`. See the Duo Admin API docs for this resource's exact schema.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = body
        try:
            result = await client.request("POST", "/admin/v2/integrations", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_integrations_delete_integration(integration_key: str) -> str:
        """Delete Integration.

        API: DELETE /admin/v2/integrations/{integration_key}

        Args:
            integration_key: Required. Path parameter `integration_key`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v2/integrations/{integration_key}"
        params = {}
        try:
            result = await client.request("DELETE", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_integrations_modify_integration(integration_key: str, name: str | None = None, networks_for_api_access: str | None = None, adminapi_admins: str | None = None, adminapi_info: str | None = None, adminapi_integrations: str | None = None, adminapi_read_log: str | None = None, adminapi_read_resource: str | None = None, adminapi_settings: str | None = None, adminapi_write_resource: str | None = None, trusted_device_days: str | None = None, enroll_policy: str | None = None, greeting: str | None = None, groups_allowed: str | None = None, ip_whitelist: str | None = None, ip_whitelist_enroll_policy: str | None = None, policy_key: str | None = None, reset_secret_key: str | None = None, self_service_allowed: str | None = None, username_normalization_policy: str | None = None) -> str:
        """Modify Integration.

        API: POST /admin/v2/integrations/[integration_key]

        Args:
            integration_key: Required. Path parameter `integration_key`.
            name: Optional. Query parameter `name`.
            networks_for_api_access: Optional. Query parameter `networks_for_api_access`.
            adminapi_admins: Optional. Query parameter `adminapi_admins`.
            adminapi_info: Optional. Query parameter `adminapi_info`.
            adminapi_integrations: Optional. Query parameter `adminapi_integrations`.
            adminapi_read_log: Optional. Query parameter `adminapi_read_log`.
            adminapi_read_resource: Optional. Query parameter `adminapi_read_resource`.
            adminapi_settings: Optional. Query parameter `adminapi_settings`.
            adminapi_write_resource: Optional. Query parameter `adminapi_write_resource`.
            trusted_device_days: Optional. Query parameter `trusted_device_days`.
            enroll_policy: Optional. Query parameter `enroll_policy`.
            greeting: Optional. Query parameter `greeting`.
            groups_allowed: Optional. Query parameter `groups_allowed`.
            ip_whitelist: Optional. Query parameter `ip_whitelist`.
            ip_whitelist_enroll_policy: Optional. Query parameter `ip_whitelist_enroll_policy`.
            policy_key: Optional. Query parameter `policy_key`.
            reset_secret_key: Optional. Query parameter `reset_secret_key`.
            self_service_allowed: Optional. Query parameter `self_service_allowed`.
            username_normalization_policy: Optional. Query parameter `username_normalization_policy`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v2/integrations/{integration_key}"
        params = {"name": name, "networks_for_api_access": networks_for_api_access, "adminapi_admins": adminapi_admins, "adminapi_info": adminapi_info, "adminapi_integrations": adminapi_integrations, "adminapi_read_log": adminapi_read_log, "adminapi_read_resource": adminapi_read_resource, "adminapi_settings": adminapi_settings, "adminapi_write_resource": adminapi_write_resource, "trusted_device_days": trusted_device_days, "enroll_policy": enroll_policy, "greeting": greeting, "groups_allowed": groups_allowed, "ip_whitelist": ip_whitelist, "ip_whitelist_enroll_policy": ip_whitelist_enroll_policy, "policy_key": policy_key, "reset_secret_key": reset_secret_key, "self_service_allowed": self_service_allowed, "username_normalization_policy": username_normalization_policy}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_integrations_modify_sso_integration(integration_key: str, body: dict) -> str:
        """Modify SSO Integration.

        API: POST /admin/v2/integrations/{integration_key}

        Args:
            integration_key: Required. Path parameter `integration_key`.
            body: Required. JSON request payload sent verbatim as the signed request body. Top-level fields (from the vendor's example): `name`, `self_service_allowed`. See the Duo Admin API docs for this resource's exact schema.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v2/integrations/{integration_key}"
        params = body
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_integrations_reset_oauth_client_secret(integration_key: str, client_id: str) -> str:
        """Reset OAUTH client secret.

        API: POST /admin/v2/integrations/oauth_cc/{integration_key}/client_secret/{client_id}

        Args:
            integration_key: Required. Path parameter `integration_key`.
            client_id: Required. Path parameter `client_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v2/integrations/oauth_cc/{integration_key}/client_secret/{client_id}"
        params = {}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_integrations_reset_oidc_client_secret(integration_key: str) -> str:
        """Reset OIDC client secret.

        API: POST /admin/v2/integrations/oidc/{integration_key}/client_secret

        Args:
            integration_key: Required. Path parameter `integration_key`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v2/integrations/oidc/{integration_key}/client_secret"
        params = {}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_integrations_retrieve_integration_by_integration_key(integration_key: str) -> str:
        """Retrieve Integration by Integration Key.

        API: GET /admin/v2/integrations/{integration_key}

        Args:
            integration_key: Required. Path parameter `integration_key`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v2/integrations/{integration_key}"
        params = {}
        try:
            result = await client.request("GET", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_integrations_retrieve_integrations(limit: str | None = None, offset: str | None = None) -> str:
        """Retrieve Integrations.

        API: GET /admin/v2/integrations

        Args:
            limit: Optional. Query parameter `limit`.
            offset: Optional. Query parameter `offset`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"limit": limit, "offset": offset}
        try:
            result = await client.request("GET", "/admin/v2/integrations", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_integrations_retrieve_oauth_client_secret(integration_key: str, client_id: str) -> str:
        """Retrieve OAUTH client secret.

        API: GET /admin/v2/integrations/oauth_cc/{integration_key}/client_secret/{client_id}

        Args:
            integration_key: Required. Path parameter `integration_key`.
            client_id: Required. Path parameter `client_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v2/integrations/oauth_cc/{integration_key}/client_secret/{client_id}"
        params = {}
        try:
            result = await client.request("GET", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_integrations_retrieve_oidc_client_secret(integration_key: str) -> str:
        """Retrieve OIDC client secret.

        API: GET /admin/v2/integrations/oidc/{integration_key}/client_secret

        Args:
            integration_key: Required. Path parameter `integration_key`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v2/integrations/oidc/{integration_key}/client_secret"
        params = {}
        try:
            result = await client.request("GET", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_integrations_retrieve_secret_key(integration_key: str) -> str:
        """Retrieve secret key.

        API: GET /admin/v1/integrations/{integration_key}/skey

        Args:
            integration_key: Required. Path parameter `integration_key`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/integrations/{integration_key}/skey"
        params = {}
        try:
            result = await client.request("GET", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"
