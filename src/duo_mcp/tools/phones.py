from collections.abc import Callable
from typing import Annotated, Literal

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .._json import dump_json_capped
from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN

# Duo's documented hard cap for GET /admin/v1/phones (duo.com/docs/adminapi).
_MAX_LIMIT = 500


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:
    @mcp.tool()
    async def duo_phones_create_activation_code_via_sms(
        phone_id: Annotated[str, Field(description="Phone ID to send the activation code to.")],
        valid_secs: Annotated[
            int | None, Field(description="Seconds the code stays valid (default 86400).")
        ] = None,
        install: Annotated[
            Literal["0", "1"] | None,
            Field(description='"1" to also send an install SMS first, "0" to skip (default "0").'),
        ] = None,
        installation_msg: Annotated[
            str | None,
            Field(description='Custom install SMS text; must contain the literal "<insturl>".'),
        ] = None,
        activation_msg: Annotated[
            str | None,
            Field(description='Custom activation SMS text; must contain the literal "<acturl>".'),
        ] = None,
    ) -> str:
        """Send an activation code to a phone via SMS."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/phones/{phone_id}/send_sms_activation"
        params = {
            "valid_secs": valid_secs,
            "install": install,
            "installation_msg": installation_msg,
            "activation_msg": activation_msg,
        }
        try:
            result = await client.request("POST", path, params=params)
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool()
    async def duo_phones_create_phone() -> str:
        """Create a new (unactivated) phone record."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.request("POST", "/admin/v1/phones", params={})
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def duo_phones_retrieve_phone_by_id(
        phone_id: Annotated[str, Field(description="Phone ID to look up.")],
    ) -> str:
        """Get a single phone's details by ID."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/phones/{phone_id}"
        try:
            result = await client.request("GET", path, params={})
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def duo_phones_retrieve_phones(
        number: Annotated[
            str | None, Field(description="Look up a single phone by number.")
        ] = None,
        extension: Annotated[str | None, Field(description="Phone extension, if any.")] = None,
        limit: Annotated[
            int | None, Field(description="Max records to return (default 100, max 500).")
        ] = None,
        offset: Annotated[
            int | None, Field(description="Offset from 0 to start record retrieval.")
        ] = None,
    ) -> str:
        """List phones in the account."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        if limit is not None:
            limit = min(limit, _MAX_LIMIT)
        params = {"number": number, "extension": extension, "limit": limit, "offset": offset}
        try:
            result = await client.request("GET", "/admin/v1/phones", params=params)
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()
