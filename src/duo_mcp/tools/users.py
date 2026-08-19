from collections.abc import Callable
from typing import Annotated, Literal

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .._json import dump_json_capped
from ..api_client import DuoClient, DuoError
from ._common import NO_TOKEN

# Duo's documented hard cap for the per-user-scoped list endpoints (groups/
# tokens/phones by user ID): default 100, max 500 (duo.com/docs/adminapi).
_MAX_LIMIT_BY_USER = 500

# GET /admin/v1/users itself has a stricter documented cap than the other
# list endpoints in this file (100 default / 300 max, not 500) — verified
# directly against duo.com/docs/adminapi. Do not reuse _MAX_LIMIT_BY_USER
# here; a value between 300 and 500 would be silently rejected by Duo.
_MAX_LIMIT_USERS = 300

_UserStatus = Literal["active", "bypass", "disabled"]


def register(mcp: FastMCP, client_factory: Callable[[], DuoClient | None]) -> None:
    @mcp.tool(annotations=ToolAnnotations(idempotentHint=True))
    async def duo_users_associate_group_with_user(
        user_id: Annotated[str, Field(description="User ID.")],
        group_id: Annotated[str, Field(description="Group ID to associate with the user.")],
    ) -> str:
        """Associate a group with a user."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/users/{user_id}/groups"
        try:
            result = await client.request("POST", path, params={"group_id": group_id})
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(idempotentHint=True))
    async def duo_users_associate_hardware_token_with_user(
        user_id: Annotated[str, Field(description="User ID.")],
        token_id: Annotated[str, Field(description="Hardware token ID to associate.")],
    ) -> str:
        """Associate a hardware token with a user."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/users/{user_id}/tokens"
        try:
            result = await client.request("POST", path, params={"token_id": token_id})
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(idempotentHint=True))
    async def duo_users_associate_phone_with_user(
        user_id: Annotated[str, Field(description="User ID.")],
        phone_id: Annotated[str, Field(description="Phone ID to associate.")],
    ) -> str:
        """Associate a phone with a user."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/users/{user_id}/phones"
        try:
            result = await client.request("POST", path, params={"phone_id": phone_id})
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool()
    async def duo_users_create_bypass_codes_for_user(
        user_id: Annotated[str, Field(description="User ID.")],
        count: Annotated[
            int | None, Field(description="Number of codes to generate (default 1, max 10).")
        ] = None,
        codes: Annotated[
            str | None,
            Field(description="CSV of specific codes to use instead of generating them."),
        ] = None,
        reuse_count: Annotated[
            int | None,
            Field(description="Times each code can be reused (0 = unlimited, default 1)."),
        ] = None,
        valid_secs: Annotated[
            int | None, Field(description="Seconds codes stay valid (0 = never expire).")
        ] = None,
    ) -> str:
        """Generate bypass codes for a user.

        `count` and `codes` are mutually exclusive.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/users/{user_id}/bypass_codes"
        params = {
            "count": count,
            "codes": codes,
            "reuse_count": reuse_count,
            "valid_secs": valid_secs,
        }
        try:
            result = await client.request("POST", path, params=params)
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool()
    async def duo_users_create_user(
        username: Annotated[str, Field(description="Username for the new user.")],
        aliases: Annotated[
            str | None,
            Field(description="Up to 8 aliases as URL-encoded pairs, e.g. alias1=a&alias2=b."),
        ] = None,
        realname: Annotated[str | None, Field(description="Full display name.")] = None,
        email: Annotated[str | None, Field(description="Email address.")] = None,
        status: Annotated[
            _UserStatus | None,
            Field(description="Enrollment status. Defaults to active if omitted."),
        ] = None,
        notes: Annotated[str | None, Field(description="Free-text notes.")] = None,
        firstname: Annotated[str | None, Field(description="Given name.")] = None,
        lastname: Annotated[str | None, Field(description="Surname.")] = None,
    ) -> str:
        """Create a new user."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {
            "username": username,
            "aliases": aliases,
            "realname": realname,
            "email": email,
            "status": status,
            "notes": notes,
            "firstname": firstname,
            "lastname": lastname,
        }
        try:
            result = await client.request("POST", "/admin/v1/users", params=params)
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(destructiveHint=True))
    async def duo_users_delete_user(
        user_id: Annotated[str, Field(description="User ID to delete.")],
    ) -> str:
        """Permanently delete a user. Irreversible — confirm the ID first."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/users/{user_id}"
        try:
            result = await client.request("DELETE", path, params={})
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(destructiveHint=True))
    async def duo_users_disassociate_phone_from_user(
        user_id: Annotated[str, Field(description="User ID.")],
        phone_id: Annotated[str, Field(description="Phone ID to remove from the user.")],
    ) -> str:
        """Remove a phone's association with a user."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/users/{user_id}/phones/{phone_id}"
        try:
            result = await client.request("DELETE", path, params={})
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool()
    async def duo_users_enroll_user(
        username: Annotated[str, Field(description="Username (or alias) to enroll.")],
        email: Annotated[str, Field(description="Email address for the enrollment link.")],
        valid_secs: Annotated[
            int | None,
            Field(description="Seconds the enrollment link stays valid (default 2592000)."),
        ] = None,
    ) -> str:
        """Send a self-enrollment link to a new user via email."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"username": username, "email": email, "valid_secs": valid_secs}
        try:
            result = await client.request("POST", "/admin/v1/users/enroll", params=params)
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(idempotentHint=True))
    async def duo_users_modify_user(
        user_id: Annotated[str, Field(description="User ID to update.")],
        username: Annotated[str | None, Field(description="New username.")] = None,
        aliases: Annotated[
            str | None,
            Field(
                description=(
                    "Up to 8 aliases as URL-encoded pairs, e.g. alias1=a&alias2=b. "
                    "Set an alias to a blank value to remove it."
                )
            ),
        ] = None,
        realname: Annotated[str | None, Field(description="New full display name.")] = None,
        email: Annotated[str | None, Field(description="New email address.")] = None,
        status: Annotated[
            _UserStatus | None, Field(description="New enrollment status.")
        ] = None,
        notes: Annotated[str | None, Field(description="New free-text notes.")] = None,
        firstname: Annotated[str | None, Field(description="New given name.")] = None,
        lastname: Annotated[str | None, Field(description="New surname.")] = None,
    ) -> str:
        """Update an existing user's profile fields."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/users/{user_id}"
        params = {
            "username": username,
            "aliases": aliases,
            "realname": realname,
            "email": email,
            "status": status,
            "notes": notes,
            "firstname": firstname,
            "lastname": lastname,
        }
        try:
            result = await client.request("POST", path, params=params)
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def duo_users_retrieve_groups_by_user_id(
        user_id: Annotated[str, Field(description="User ID.")],
        limit: Annotated[
            int | None, Field(description="Max records to return (default 100, max 500).")
        ] = None,
        offset: Annotated[
            int | None, Field(description="Offset from 0 to start record retrieval.")
        ] = None,
    ) -> str:
        """List a user's group memberships."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        if limit is not None:
            limit = min(limit, _MAX_LIMIT_BY_USER)
        path = f"/admin/v1/users/{user_id}/groups"
        params = {"limit": limit, "offset": offset}
        try:
            result = await client.request("GET", path, params=params)
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def duo_users_retrieve_hardware_tokens_by_user_id(
        user_id: Annotated[str, Field(description="User ID.")],
        limit: Annotated[
            int | None, Field(description="Max records to return (default 100, max 500).")
        ] = None,
        offset: Annotated[
            int | None, Field(description="Offset from 0 to start record retrieval.")
        ] = None,
    ) -> str:
        """List hardware tokens enrolled for a user."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        if limit is not None:
            limit = min(limit, _MAX_LIMIT_BY_USER)
        path = f"/admin/v1/users/{user_id}/tokens"
        params = {"limit": limit, "offset": offset}
        try:
            result = await client.request("GET", path, params=params)
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def duo_users_retrieve_phones_by_user_id(
        user_id: Annotated[str, Field(description="User ID.")],
        limit: Annotated[
            int | None, Field(description="Max records to return (default 100, max 500).")
        ] = None,
        offset: Annotated[
            int | None, Field(description="Offset from 0 to start record retrieval.")
        ] = None,
    ) -> str:
        """List phones enrolled for a user."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        if limit is not None:
            limit = min(limit, _MAX_LIMIT_BY_USER)
        path = f"/admin/v1/users/{user_id}/phones"
        params = {"limit": limit, "offset": offset}
        try:
            result = await client.request("GET", path, params=params)
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def duo_users_retrieve_user_by_id(
        user_id: Annotated[str, Field(description="User ID to look up.")],
    ) -> str:
        """Get a single user's details by ID."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/users/{user_id}"
        try:
            result = await client.request("GET", path, params={})
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def duo_users_retrieve_users(
        username: Annotated[
            str | None, Field(description="Look up a single user by username (or alias).")
        ] = None,
        limit: Annotated[
            int | None, Field(description="Max records to return (default 100, max 300).")
        ] = None,
        offset: Annotated[
            int | None, Field(description="Offset from 0 to start record retrieval.")
        ] = None,
    ) -> str:
        """List users in the account, or look one up by username."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        if limit is not None:
            limit = min(limit, _MAX_LIMIT_USERS)
        params = {"username": username, "limit": limit, "offset": offset}
        try:
            result = await client.request("GET", "/admin/v1/users", params=params)
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def duo_users_retrieve_verification_push_response(
        user_id: Annotated[str, Field(description="User ID.")],
        push_id: Annotated[
            str, Field(description="Push ID returned by duo_users_send_verification_push.")
        ],
    ) -> str:
        """Get the result of a previously sent verification push."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/users/{user_id}/verification_push_response"
        try:
            result = await client.request("GET", path, params={"push_id": push_id})
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def duo_users_retrieve_web_authn_credentials_by_user_id(
        user_id: Annotated[str, Field(description="User ID.")],
    ) -> str:
        """List WebAuthn credentials enrolled for a user."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/users/{user_id}/webauthncredentials"
        try:
            result = await client.request("GET", path, params={})
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool()
    async def duo_users_send_verification_push(
        user_id: Annotated[str, Field(description="User ID to push the request to.")],
        phone_id: Annotated[str, Field(description="Phone ID to receive the Duo Push.")],
    ) -> str:
        """Send a Duo Push verification request to a user's phone.

        Use duo_users_retrieve_verification_push_response with the returned
        push ID to check whether the user approved it.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/users/{user_id}/send_verification_push"
        try:
            result = await client.request("POST", path, params={"phone_id": phone_id})
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(idempotentHint=True))
    async def duo_users_synchronize_user_from_directory(
        directory_key: Annotated[str, Field(description="Directory sync key.")],
        username: Annotated[
            str, Field(description="Username to sync, matching the source directory.")
        ],
    ) -> str:
        """Re-sync a user's record from a linked directory (e.g. Active Directory)."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        path = f"/admin/v1/users/directorysync/{directory_key}/syncuser"
        try:
            result = await client.request("POST", path, params={"username": username})
            return dump_json_capped(result)
        except DuoError as e:
            return e.to_envelope()
