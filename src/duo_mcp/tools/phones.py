import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:

    @mcp.tool()
    async def duo_phones_associate_phone_with_user(user_id: str, phone_id: str) -> str:
        """Associate Phone with User.

        API: POST /admin/v1/users/{user_id}/phones

        Args:
            user_id: Required. Path parameter `user_id`.
            phone_id: Required. The ID of the phone to associate with the user.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/users/{user_id}/phones"
        params = {"phone_id": phone_id}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_phones_create_activation_code(phone_id: str, valid_secs: str | None = None, install: str | None = None) -> str:
        """Create Activation Code.

        API: POST /admin/v1/phones/{phone_id}/activation_url

        Args:
            phone_id: Required. Path parameter `phone_id`.
            valid_secs: Optional. The number of seconds this activation code should be valid for. Default: 86400 (one day).
            install: Optional. “1” to also return an installation URL for Duo Mobile; “0” to not return. Default: “0”.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/phones/{phone_id}/activation_url"
        params = {"valid_secs": valid_secs, "install": install}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_phones_create_activation_code_via_sms(phone_id: str, valid_secs: str | None = None, install: str | None = None, installation_msg: str | None = None, activation_msg: str | None = None) -> str:
        """Create Activation Code via SMS.

        API: POST /admin/v1/phones/{phone_id}/send_sms_activation

        Args:
            phone_id: Required. Path parameter `phone_id`.
            valid_secs: Optional. The number of seconds this activation code should be valid for. Default: 86400 (one day).
            install: Optional. “1” to cause an installation SMS message to be sent before the activation message, “0” to not send an installation SMS message. Default: “0”.
            installation_msg: Optional. A custom installation message to send to the user. Only valid if installation was requested. Must contain the phrase “<insturl>”, which is replaced with the installation URL.
            activation_msg: Optional. A custom activation message to send to the user. Must contain “<acturl>”, which is replaced with the activation URL.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/phones/{phone_id}/send_sms_activation"
        params = {"valid_secs": valid_secs, "install": install, "installation_msg": installation_msg, "activation_msg": activation_msg}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_phones_create_phone() -> str:
        """Create Phone.

        API: POST /admin/v1/phones

        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.request("POST", "/admin/v1/phones", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_phones_delete_phone(phone_id: str) -> str:
        """Delete Phone.

        API: DELETE /admin/v1/phones/{phone_id}

        Args:
            phone_id: Required. Path parameter `phone_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/phones/{phone_id}"
        params = {}
        try:
            result = await client.request("DELETE", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_phones_disassociate_phone_from_user(user_id: str, phone_id: str) -> str:
        """Disassociate Phone from User.

        API: DELETE /admin/v1/users/{user_id}/phones/{phone_id}

        Args:
            user_id: Required. Path parameter `user_id`.
            phone_id: Required. Path parameter `phone_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/users/{user_id}/phones/{phone_id}"
        params = {}
        try:
            result = await client.request("DELETE", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_phones_modify_phone(phone_id: str, number: str | None = None, name: str | None = None, extension: str | None = None, type: str | None = None, platform: str | None = None, predelay: str | None = None, postdelay: str | None = None) -> str:
        """Modify Phone.

        API: POST /admin/v1/phones/{phone_id}

        Args:
            phone_id: Required. Path parameter `phone_id`.
            number: Optional. The new number.
            name: Optional. Free-form label for the phone.
            extension: Optional. The new extension.
            type: Optional. The type of phone. One of: “unknown”, “mobile”, or “landline”.
            platform: Optional. The phone platform. One of: “unknown”, “google android”, “apple ios”, “windows phone 7”, “rim blackberry”, “java j2me”, “palm webos”, “symbian os”, “windows mobile”, or “generic smartphone”. “windows phone” is accepted as a synonym for “windows phone 7”. This includes devices running Windows Phone 8. If a smartphone’s exact platform is unknown but it will have Duo Mobile installed, use “generic smartphone” and generate an activation code. When the phone is activated its platform will be automatically detected.
            predelay: Optional. The time (in seconds) to wait after the number picks up and before dialing the extension.
            postdelay: Optional. The time (in seconds) to wait after the extension is dialed and before the speaking the prompt.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/phones/{phone_id}"
        params = {"number": number, "name": name, "extension": extension, "type": type, "platform": platform, "predelay": predelay, "postdelay": postdelay}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_phones_retrieve_phone_by_id(phone_id: str) -> str:
        """Retrieve Phone by ID.

        API: GET /admin/v1/phones/{phone_id}

        Args:
            phone_id: Required. Path parameter `phone_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/phones/{phone_id}"
        params = {}
        try:
            result = await client.request("GET", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_phones_retrieve_phones(number: str | None = None, extension: str | None = None, limit: str | None = None, offset: str | None = None) -> str:
        """Retrieve Phones.

        API: GET /admin/v1/phones

        Args:
            number: Optional. Specify a phone number to look up a single phone.
            extension: Optional. The extension, if necessary.
            limit: Optional. The maximum number of records returned. Default: 100; Max: 500
            offset: Optional. The offset from 0 at which to start record retrieval. When used with "limit", the handler will return "limit" records starting at the n-th record, where n is the offset. Default: 0
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"number": number, "extension": extension, "limit": limit, "offset": offset}
        try:
            result = await client.request("GET", "/admin/v1/phones", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_phones_retrieve_phones_by_user_id(user_id: str, limit: str | None = None, offset: str | None = None) -> str:
        """Retrieve Phones by User ID.

        API: GET /admin/v1/users/{user_id}/phones

        Args:
            user_id: Required. Path parameter `user_id`.
            limit: Optional. The maximum number of records returned. Default: 100; Max: 500
            offset: Optional. The offset from 0 at which to start record retrieval. When used with "limit", the handler will return "limit" records starting at the n-th record, where n is the offset. Default: 0
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/users/{user_id}/phones"
        params = {"limit": limit, "offset": offset}
        try:
            result = await client.request("GET", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_phones_send_installation_url_via_sms(phone_id: str, installation_msg: str | None = None) -> str:
        """Send Installation URL via SMS.

        API: POST /admin/v1/phones/{phone_id}/send_sms_installation

        Args:
            phone_id: Required. Path parameter `phone_id`.
            installation_msg: Optional. A custom installation message to send to the user. Must contain the phrase “<insturl>”, which is replaced with the installation URL.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/phones/{phone_id}/send_sms_installation"
        params = {"installation_msg": installation_msg}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_phones_send_passcodes_via_sms(phone_id: str) -> str:
        """Send Passcodes via SMS.

        API: POST /admin/v1/phones/{phone_id}/send_sms_passcodes

        Args:
            phone_id: Required. Path parameter `phone_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/phones/{phone_id}/send_sms_passcodes"
        params = {}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"
