"""tools/list snapshot + error-envelope mapping tests.

No network calls: tool enumeration goes through FastMCP's in-process
list_tools(), and the error-code mapping is tested directly against
DuoError, independent of any real HTTP request.
"""

import pytest

from duo_mcp.api_client import DuoError
from duo_mcp.config import Settings
from duo_mcp.server import create_mcp_server

# name -> required (non-default) parameter names
EXPECTED_TOOLS: dict[str, set[str]] = {
    "duo_groups_get_group_info": {"group_id"},
    "duo_groups_retrieve_groups": set(),
    "duo_logs_administrator_logs": set(),
    "duo_phones_create_activation_code_via_sms": {"phone_id"},
    "duo_phones_create_phone": set(),
    "duo_phones_retrieve_phone_by_id": {"phone_id"},
    "duo_phones_retrieve_phones": set(),
    "duo_tokens_retrieve_hardware_token_by_id": {"token_id"},
    "duo_tokens_retrieve_hardware_tokens": set(),
    "duo_users_associate_group_with_user": {"user_id", "group_id"},
    "duo_users_associate_hardware_token_with_user": {"user_id", "token_id"},
    "duo_users_associate_phone_with_user": {"user_id", "phone_id"},
    "duo_users_create_bypass_codes_for_user": {"user_id"},
    "duo_users_create_user": {"username"},
    "duo_users_delete_user": {"user_id"},
    "duo_users_disassociate_phone_from_user": {"user_id", "phone_id"},
    "duo_users_enroll_user": {"username", "email"},
    "duo_users_modify_user": {"user_id"},
    "duo_users_retrieve_groups_by_user_id": {"user_id"},
    "duo_users_retrieve_hardware_tokens_by_user_id": {"user_id"},
    "duo_users_retrieve_phones_by_user_id": {"user_id"},
    "duo_users_retrieve_user_by_id": {"user_id"},
    "duo_users_retrieve_users": set(),
    "duo_users_retrieve_verification_push_response": {"user_id", "push_id"},
    "duo_users_retrieve_web_authn_credentials_by_user_id": {"user_id"},
    "duo_users_send_verification_push": {"user_id", "phone_id"},
    "duo_users_synchronize_user_from_directory": {"directory_key", "username"},
    "duo_webauthn_credentials_retrieve_web_authn_credentials": set(),
    "duo_webauthn_credentials_retrieve_web_authn_credentials_by_key": {"webauthnkey"},
}

READ_ONLY_TOOLS = {
    "duo_groups_get_group_info",
    "duo_groups_retrieve_groups",
    "duo_logs_administrator_logs",
    "duo_phones_retrieve_phone_by_id",
    "duo_phones_retrieve_phones",
    "duo_tokens_retrieve_hardware_token_by_id",
    "duo_tokens_retrieve_hardware_tokens",
    "duo_users_retrieve_groups_by_user_id",
    "duo_users_retrieve_hardware_tokens_by_user_id",
    "duo_users_retrieve_phones_by_user_id",
    "duo_users_retrieve_user_by_id",
    "duo_users_retrieve_users",
    "duo_users_retrieve_verification_push_response",
    "duo_users_retrieve_web_authn_credentials_by_user_id",
    "duo_webauthn_credentials_retrieve_web_authn_credentials",
    "duo_webauthn_credentials_retrieve_web_authn_credentials_by_key",
}

DESTRUCTIVE_TOOLS = {
    "duo_users_delete_user",
    "duo_users_disassociate_phone_from_user",
}

IDEMPOTENT_TOOLS = {
    "duo_users_associate_group_with_user",
    "duo_users_associate_hardware_token_with_user",
    "duo_users_associate_phone_with_user",
    "duo_users_modify_user",
    "duo_users_synchronize_user_from_directory",
}


@pytest.mark.asyncio
async def test_tools_list_snapshot():
    mcp = create_mcp_server(Settings())
    tools = await mcp.list_tools()
    names = {t.name for t in tools}
    assert names == set(EXPECTED_TOOLS), f"unexpected tool set: {names}"

    by_name = {t.name: t for t in tools}
    for name, expected_required in EXPECTED_TOOLS.items():
        tool = by_name[name]
        required = set(tool.inputSchema.get("required", []))
        assert required == expected_required, f"{name}: required={required}"

        assert len(tool.description or "") <= 500, f"{name}: description too long"
        first_line = (tool.description or "").strip().splitlines()[0]
        assert len(first_line) <= 100, f"{name}: first line too long: {first_line!r}"
        assert "API:" not in (tool.description or ""), f"{name}: leaked implementation detail"

        ann = tool.annotations
        if name in READ_ONLY_TOOLS:
            assert ann is not None and ann.readOnlyHint is True, f"{name}: expected readOnlyHint"
        if name in DESTRUCTIVE_TOOLS:
            assert ann is not None and ann.destructiveHint is True, (
                f"{name}: expected destructiveHint"
            )
        if name in IDEMPOTENT_TOOLS:
            assert ann is not None and ann.idempotentHint is True, (
                f"{name}: expected idempotentHint"
            )


@pytest.mark.asyncio
async def test_service_instructions_present_and_bounded():
    mcp = create_mcp_server(Settings())
    assert mcp.instructions
    assert len(mcp.instructions) <= 1500


@pytest.mark.parametrize(
    "status_code,expected_code,expected_retryable",
    [
        (0, "upstream_error", True),
        (400, "invalid_argument", False),
        (401, "unauthorized", False),
        (403, "unauthorized", False),
        (404, "not_found", False),
        (422, "invalid_argument", False),
        (429, "rate_limited", True),
        (500, "upstream_error", True),
        (503, "upstream_error", True),
    ],
)
def test_error_envelope_mapping(status_code, expected_code, expected_retryable):
    import json

    err = DuoError(status_code, "boom")
    envelope = json.loads(err.to_envelope())
    assert envelope["error"]["code"] == expected_code
    assert envelope["error"]["retryable"] is expected_retryable
    assert envelope["error"]["message"] == "boom"
