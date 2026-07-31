import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:

    @mcp.tool()
    async def duo_custom_branding_add_draft_custom_branding_user_by_id(user_id: str) -> str:
        """Add Draft Custom Branding User by ID.

        API: POST /admin/v1/branding/draft/users/{user_id}

        Args:
            user_id: Required. Path parameter `user_id`.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/branding/draft/users/{user_id}"
        params = {}
        try:
            result = await client.request("POST", path, params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_custom_branding_modify_custom_messaging() -> str:
        """Modify Custom Messaging.

        API: POST /admin/v1/branding/custom_messaging

        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.request("POST", "/admin/v1/branding/custom_messaging", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_custom_branding_modify_draft_custom_branding() -> str:
        """Modify Draft Custom Branding.

        API: POST /admin/v1/branding/draft

        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.request("POST", "/admin/v1/branding/draft", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_custom_branding_modify_live_custom_branding() -> str:
        """Modify Live Custom Branding.

        API: POST /admin/v1/branding

        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.request("POST", "/admin/v1/branding", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_custom_branding_publish_draft_custom_branding() -> str:
        """Publish Draft Custom Branding.

        API: POST /admin/v1/branding/draft/publish

        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.request("POST", "/admin/v1/branding/draft/publish", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_custom_branding_retrieve_custom_messaging() -> str:
        """Retrieve Custom Messaging.

        API: GET /admin/v1/branding/custom_messaging

        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.request("GET", "/admin/v1/branding/custom_messaging", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_custom_branding_retrieve_draft_custom_branding() -> str:
        """Retrieve Draft Custom Branding.

        API: GET /admin/v1/branding/draft

        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.request("GET", "/admin/v1/branding/draft", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def duo_custom_branding_retrieve_live_custom_branding() -> str:
        """Retrieve Live Custom Branding.

        API: GET /admin/v1/branding

        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.request("GET", "/admin/v1/branding", params=params)
            return json.dumps(result, indent=2, default=str)
        except DuoError as e:
            return f"Error: {e}"
