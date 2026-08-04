import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:
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

