import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:

    @mcp.tool()
    async def duo_administrators_clear_administrator_expiration(admin_id: str) -> str:
        """Clear Administrator Expiration.

        API: POST /admin/v1/admins/{admin_id}/clear_inactivity

        Args:
            admin_id: Required. Path parameter `admin_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/admins/{admin_id}/clear_inactivity"
        params = {}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrators_create_activation_link_for_administrator_pending_activation(admin_id: str) -> str:
        """Create Activation Link for Administrator Pending Activation.

        API: POST /admin/v1/admins/[admin_id]/activation_link

        Args:
            admin_id: Required. Path parameter `admin_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/admins/{admin_id}/activation_link"
        params = {}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrators_create_administrator_activation_link(email: str, admin_name: str | None = None, admin_role: str | None = None, send_email: str | None = None, valid_days: str | None = None) -> str:
        """Create Administrator Activation Link.

        API: POST /admin/v1/admins/activations

        Args:
            email: Required. Query parameter `email`.
            admin_name: Optional. Query parameter `admin_name`.
            admin_role: Optional. Query parameter `admin_role`.
            send_email: Optional. Query parameter `send_email`.
            valid_days: Optional. Query parameter `valid_days`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"email": email, "admin_name": admin_name, "admin_role": admin_role, "send_email": send_email, "valid_days": valid_days}
        try:
            result = await client.request("POST", "/admin/v1/admins/activations", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrators_create_administrators(email: str, name: str, phone: str | None = None, role: str | None = None, restricted_by_admin_units: str | None = None, send_email: str | None = None, token_id: str | None = None, valid_days: str | None = None) -> str:
        """Create Administrators.

        API: POST /admin/v1/admins

        Args:
            email: Required. Query parameter `email`.
            name: Required. Query parameter `name`.
            phone: Optional. Query parameter `phone`.
            role: Optional. Query parameter `role`.
            restricted_by_admin_units: Optional. Query parameter `restricted_by_admin_units`.
            send_email: Optional. Query parameter `send_email`.
            token_id: Optional. Query parameter `token_id`.
            valid_days: Optional. Query parameter `valid_days`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"email": email, "name": name, "phone": phone, "role": role, "restricted_by_admin_units": restricted_by_admin_units, "send_email": send_email, "token_id": token_id, "valid_days": valid_days}
        try:
            result = await client.request("POST", "/admin/v1/admins", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrators_delete_activation_link_to_administrator_pending_activation(admin_id: str) -> str:
        """Delete Activation Link to Administrator Pending Activation.

        API: DELETE /admin/v1/admins/[admin_id]/activation_link

        Args:
            admin_id: Required. Path parameter `admin_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/admins/{admin_id}/activation_link"
        params = {}
        try:
            result = await client.request("DELETE", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrators_delete_administrator(admin_id: str) -> str:
        """Delete Administrator.

        API: DELETE /admin/v1/admins/[admin_id]

        Args:
            admin_id: Required. Path parameter `admin_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/admins/{admin_id}"
        params = {}
        try:
            result = await client.request("DELETE", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrators_delete_pending_administrator_activation(admin_activation_id: str) -> str:
        """Delete Pending Administrator Activation.

        API: DELETE /admin/v1/admins/activations/[admin_activation_id]

        Args:
            admin_activation_id: Required. Path parameter `admin_activation_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/admins/activations/{admin_activation_id}"
        params = {}
        try:
            result = await client.request("DELETE", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrators_email_activation_link_to_administrator_pending_activation(admin_id: str) -> str:
        """Email Activation Link to Administrator Pending Activation.

        API: POST /admin/v1/admins/[admin_id]/activation_link/email

        Args:
            admin_id: Required. Path parameter `admin_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/admins/{admin_id}/activation_link/email"
        params = {}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrators_modify_admin_external_password_management_status_or_password(admin_id: str, has_external_password_mgmt: str | None = None, password: str | None = None) -> str:
        """Modify Admin External Password Management Status or Password.

        API: POST /admin/v1/admins/[admin_id]/password_mgmt

        Args:
            admin_id: Required. Path parameter `admin_id`.
            has_external_password_mgmt: Optional. Query parameter `has_external_password_mgmt`.
            password: Optional. Query parameter `password`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/admins/{admin_id}/password_mgmt"
        params = {"has_external_password_mgmt": has_external_password_mgmt, "password": password}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrators_modify_administrator(admin_id: str, name: str | None = None, phone: str | None = None, password_change_required: str | None = None, role: str | None = None, restricted_by_admin_units: str | None = None, status: str | None = None, token_id: str | None = None) -> str:
        """Modify Administrator.

        API: POST /admin/v1/admins/[admin_id]

        Args:
            admin_id: Required. Path parameter `admin_id`.
            name: Optional. Query parameter `name`.
            phone: Optional. Query parameter `phone`.
            password_change_required: Optional. Query parameter `password_change_required`.
            role: Optional. Query parameter `role`.
            restricted_by_admin_units: Optional. Query parameter `restricted_by_admin_units`.
            status: Optional. Query parameter `status`.
            token_id: Optional. Query parameter `token_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/admins/{admin_id}"
        params = {"name": name, "phone": phone, "password_change_required": password_change_required, "role": role, "restricted_by_admin_units": restricted_by_admin_units, "status": status, "token_id": token_id}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrators_reset_administrator_authentication_attempts(admin_id: str) -> str:
        """Reset Administrator Authentication Attempts.

        API: POST /admin/v1/admins/[admin_id]/reset

        Args:
            admin_id: Required. Path parameter `admin_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/admins/{admin_id}/reset"
        params = {}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrators_restrict_administrator_authentication_factors(hardware_token_enabled: str | None = None, mobile_otp_enabled: str | None = None, push_enabled: str | None = None, sms_enabled: str | None = None, voice_enabled: str | None = None, yubikey_enabled: str | None = None) -> str:
        """Restrict Administrator Authentication Factors.

        API: POST /admin/v1/admins/allowed_auth_methods

        Args:
            hardware_token_enabled: Optional. Query parameter `hardware_token_enabled`.
            mobile_otp_enabled: Optional. Query parameter `mobile_otp_enabled`.
            push_enabled: Optional. Query parameter `push_enabled`.
            sms_enabled: Optional. Query parameter `sms_enabled`.
            voice_enabled: Optional. Query parameter `voice_enabled`.
            yubikey_enabled: Optional. Query parameter `yubikey_enabled`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"hardware_token_enabled": hardware_token_enabled, "mobile_otp_enabled": mobile_otp_enabled, "push_enabled": push_enabled, "sms_enabled": sms_enabled, "voice_enabled": voice_enabled, "yubikey_enabled": yubikey_enabled}
        try:
            result = await client.request("POST", "/admin/v1/admins/allowed_auth_methods", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrators_retrieve_admin_external_password_management_status(limit: str | None = None, offset: str | None = None) -> str:
        """Retrieve Admin External Password Management Status.

        API: GET /admin/v1/admins/password_mgmt

        Args:
            limit: Optional. Query parameter `limit`.
            offset: Optional. Query parameter `offset`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"limit": limit, "offset": offset}
        try:
            result = await client.request("GET", "/admin/v1/admins/password_mgmt", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrators_retrieve_admin_external_password_management_status_by_id(admin_id: str) -> str:
        """Retrieve Admin External Password Management Status by ID.

        API: GET /admin/v1/admins/[admin_id]/password_mgmt

        Args:
            admin_id: Required. Path parameter `admin_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/admins/{admin_id}/password_mgmt"
        params = {}
        try:
            result = await client.request("GET", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrators_retrieve_administrator_authentication_factors() -> str:
        """Retrieve Administrator Authentication Factors.

        API: GET /admin/v1/admins/allowed_auth_methods

        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.request("GET", "/admin/v1/admins/allowed_auth_methods", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrators_retrieve_administrator_by_id(admin_id: str) -> str:
        """Retrieve Administrator by ID.

        API: GET /admin/v1/admins/[admin_id]

        Args:
            admin_id: Required. Path parameter `admin_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/admins/{admin_id}"
        params = {}
        try:
            result = await client.request("GET", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrators_retrieve_administrators(limit: str | None = None, offset: str | None = None) -> str:
        """Retrieve Administrators.

        API: GET /admin/v1/admins

        Args:
            limit: Optional. Query parameter `limit`.
            offset: Optional. Query parameter `offset`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"limit": limit, "offset": offset}
        try:
            result = await client.request("GET", "/admin/v1/admins", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrators_retrieve_pending_administrator_activation(limit: str | None = None, offset: str | None = None) -> str:
        """Retrieve Pending Administrator Activation.

        API: GET /admin/v1/admins/activations

        Args:
            limit: Optional. Query parameter `limit`.
            offset: Optional. Query parameter `offset`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"limit": limit, "offset": offset}
        try:
            result = await client.request("GET", "/admin/v1/admins/activations", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_administrators_sync_admin_from_directory(directory_key: str, email: str) -> str:
        """Sync Admin from directory.

        API: POST /admin/v1/admins/directorysync/{directory_key}/syncadmin

        Args:
            directory_key: Required. Path parameter `directory_key`.
            email: Required. Email address of admin to sync
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/admins/directorysync/{directory_key}/syncadmin"
        params = {"email": email}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"
