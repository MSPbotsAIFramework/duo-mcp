# duo-mcp

MCP server for the **Cisco Duo Admin API** — Duo's multi-factor authentication
and zero-trust access platform. Built to cover MFA synchronization, user
pre-enrollment, and enrollment validation (the capabilities this task
specifically requested), and — per an explicit follow-up scope decision — the
**full Admin API** beyond that.

## Overview

- Stateless HTTP service. No credentials are ever persisted — each request
  supplies its own integration key/secret key/API host via headers, used only
  for the lifetime of that single request.
- Supports concurrent requests; per-request credential isolation is done via
  Python `contextvars`, not a global/shared client instance.
- Entry points: `POST /mcp` (MCP protocol) and `GET /health` (health check).
- Default port: `8080` (configurable via `MCP_HTTP_PORT`).

## Scope

**160 tools** across 20 categories (Users, Groups, Phones, Tokens, WebAuthn
Credentials, Desktop Authenticators, Bypass Codes, Integrations, Policies,
Endpoints, Registered Devices, Passport, Administrators, Administrative
Units, Logs, Trust Monitor, Settings, Custom Branding, Account Info, Bulk
Operations).

**No MSPbots-existing integration to anchor scope against** — Duo was not
previously configured in MSPbots' integration platform, and the ClickUp task
itself only asked for MFA sync / pre-enrollment / enrollment validation. Per
explicit follow-up decision, this build covers the **entire public Admin
API**, matching the pattern used for other large-API vendors in this
program.

**No official Duo MCP exists** — searched GitHub (`duo-mcp`, `"duosecurity"
mcp`) and both `wyre-technology`/`MSPbotsAI` orgs before building; the only
existing "Duo + MCP" material is [Duo SSO for MCP](https://duo.com/docs/sso-oauth-server-mcp),
which is the reverse relationship (Duo as an identity provider *protecting*
MCP servers), not a Duo Admin API MCP server.

Source data was extracted from Duo's own official Postman collection
(`https://github.com/duosecurity/duo_postman_collection`, `duo-admin-api`
folder — cloned locally and parsed), cross-referenced against the live
`duo.com/docs/adminapi` documentation for required/optional parameter flags.

## Authentication

Duo Admin API auth is **not** a simple bearer token — every request is
individually signed with **HMAC-SHA512** (Duo's "sig_version 5") using an
Integration Key (`ikey`) and Secret Key (`skey`). This server implements
that signing logic itself (ported line-for-line from Duo's own
[reference Python client](https://github.com/duosecurity/duo_client_python)
and **verified byte-for-byte identical** against that reference
implementation for both GET-style query-signed requests and POST-style
JSON-body-signed requests, including special-character percent-encoding) —
callers only need to supply the raw ikey/skey/host per request; this server
computes the canonical string, HMAC, and `Authorization: Basic` header on
every call.

Per Duo's own signing convention: `GET`/`DELETE` requests sign and send
params as a url-encoded query string; `POST`/`PUT`/`PATCH` requests sign and
send params as a single JSON object request body. Tools in this server don't
need to know which — the client picks the correct transport based on the
HTTP method automatically, exactly matching the reference implementation's
behavior.

### HEADER 授权参数说明

| Header | 类型 | 是否必填 | 默认值 | 枚举值 | 字段描述 | Example |
|---|---|---|---|---|---|---|
| `X-Duo-Ikey` | string | 是 | 无 | 无 | Duo Admin API 集成的 Integration Key（用作 HMAC 签名的 Basic Auth 用户名部分） | `X-Duo-Ikey: DIABCDEFGHIJ1234567K` |
| `X-Duo-Skey` | string | 是 | 无 | 无 | Duo Admin API 集成的 Secret Key（HMAC-SHA512 签名密钥，仅用于当次请求签名计算，不落盘） | `X-Duo-Skey: 1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b` |
| `X-Duo-Api-Host` | string | 是 | 无 | 无 | 该 Duo 账号的 Admin API host（每个账号独立子域名，如 `api-xxxxxxxx.duosecurity.com`），无需带协议前缀 | `X-Duo-Api-Host: api-12345678.duosecurity.com` |

Missing any header returns `401`:
```json
{
  "error": "Missing credentials",
  "message": "This server requires the X-Duo-Ikey, X-Duo-Skey, and X-Duo-Api-Host headers",
  "required_headers": ["X-Duo-Ikey", "X-Duo-Skey", "X-Duo-Api-Host"],
  "optional_headers": []
}
```

## Environment Variables

| Variable | 类型 | 是否必填 | 默认值 | 说明 |
|---|---|---|---|---|
| `MCP_HTTP_PORT` | int | 否 | `8080` | HTTP 监听端口 |
| `MCP_HTTP_HOST` | string | 否 | `0.0.0.0` | HTTP 监听地址 |

## MCP Endpoint

- `POST /mcp` — MCP protocol (streamable HTTP transport)
- `GET /health` — health check, returns `{"status": "ok", "service": "duo-mcp", "transport": "http"}`

## Tool List

Tool names are `duo_<category>_<operation>`, derived from each operation's
name in Duo's official Postman collection. `body` parameters (for endpoints
whose payload is a nested/complex JSON object rather than flat scalar
fields, e.g. bulk operations, SSO integration config, policy sections) are
accepted as a generic `dict` — the docstring lists the top-level keys from
Duo's own example, and the full schema is in the linked API reference.

The 3 capabilities this task specifically named map to these tools:
- **MFA synchronization**: `duo_users_retrieve_users`, `duo_users_synchronize_user_from_directory`
- **User pre-enrollment**: `duo_users_create_user`, `duo_users_enroll_user`
- **Enrollment validation**: `duo_users_send_verification_push` + `duo_users_retrieve_verification_push_response`

| Category | Tool | 功能 | 方法+路径 | 参数 |
|---|---|---|---|---|
| account_info | `duo_account_info_authentication_attempts_report` | Authentication Attempts Report. | GET /admin/v1/info/authentication_attempts | maxtime(可选), mintime(可选) |
| account_info | `duo_account_info_retrieve_summary` | Retrieve Summary. | GET /admin/v1/users | username(可选), limit(可选), offset(可选) |
| account_info | `duo_account_info_telephony_credits_used_report_copy` | Telephony Credits Used Report Copy. | GET /admin/v1/users | username(可选), limit(可选), offset(可选) |
| account_info | `duo_account_info_users_with_authentication_attempts_report` | Users with Authentication Attempts Report. | GET /admin/v1/info/user_authentication_attempts | maxtime(可选), mintime(可选) |
| administrative_units | `duo_administrative_units_add_administrative_unit` | Add Administrative Unit. | POST /admin/v1/administrative_units | name(必填), description(必填), restrict_by_groups(可选), restrict_by_integrations(可选), admins(可选), groups(可选), integrations(可选) |
| administrative_units | `duo_administrative_units_add_administrator_to_administrative_unit` | Add Administrator to Administrative Unit. | POST /admin/v1/administrative_units/[admin_unit_id]/admin/[admin_id] | admin_unit_id(必填), admin_id(必填) |
| administrative_units | `duo_administrative_units_add_group_to_administrative_unit` | Add Group to Administrative Unit. | POST /admin/v1/administrative_units/[admin_unit_id]/group/[goup_id] | admin_unit_id(必填), goup_id(必填) |
| administrative_units | `duo_administrative_units_add_integration_to_administrative_unit` | Add Integration to Administrative Unit. | POST /admin/v1/administrative_units/[admin_unit_id]/integration/[integration_key] | admin_unit_id(必填), integration_key(必填) |
| administrative_units | `duo_administrative_units_delete_administrative_unit` | Delete Administrative Unit. | DELETE /admin/v1/administrative_units/[admin_unit_id] | admin_unit_id(必填) |
| administrative_units | `duo_administrative_units_modify_administrative_unit` | Modify Administrative Unit. | POST /admin/v1/administrative_units/[admin_unit_id] | admin_unit_id(必填), name(可选), description(可选), restrict_by_groups(可选), restrict_by_integrations(可选), admins(可选), groups(可选), integrations(可选) |
| administrative_units | `duo_administrative_units_remove_administrator_from_administrative_unit` | Remove Administrator from Administrative Unit. | DELETE /admin/v1/administrative_units/[admin_unit_id]/admin/[admin_id] | admin_unit_id(必填), admin_id(必填) |
| administrative_units | `duo_administrative_units_remove_group_from_administrative_unit` | Remove Group from Administrative Unit. | DELETE /admin/v1/administrative_units/[admin_unit_id]/group/[goup_id] | admin_unit_id(必填), goup_id(必填) |
| administrative_units | `duo_administrative_units_remove_integration_from_administrative_unit` | Remove Integration from Administrative Unit. | DELETE /admin/v1/administrative_units/[admin_unit_id]/integration/[integration_key] | admin_unit_id(必填), integration_key(必填) |
| administrative_units | `duo_administrative_units_retrieve_administrative_unit_details` | Retrieve Administrative Unit Details. | GET /admin/v1/administrative_units/[admin_unit_id] | admin_unit_id(必填) |
| administrative_units | `duo_administrative_units_retrieve_administrative_units` | Retrieve Administrative Units. | GET /admin/v1/administrative_units | admin_id(可选), group_id(可选), integration_key(可选), limit(可选), offset(可选) |
| administrators | `duo_administrators_clear_administrator_expiration` | Clear Administrator Expiration. | POST /admin/v1/admins/{admin_id}/clear_inactivity | admin_id(必填) |
| administrators | `duo_administrators_create_activation_link_for_administrator_pending_activation` | Create Activation Link for Administrator Pending Activation. | POST /admin/v1/admins/[admin_id]/activation_link | admin_id(必填) |
| administrators | `duo_administrators_create_administrator_activation_link` | Create Administrator Activation Link. | POST /admin/v1/admins/activations | email(必填), admin_name(可选), admin_role(可选), send_email(可选), valid_days(可选) |
| administrators | `duo_administrators_create_administrators` | Create Administrators. | POST /admin/v1/admins | email(必填), name(必填), phone(可选), role(可选), restricted_by_admin_units(可选), send_email(可选), token_id(可选), valid_days(可选) |
| administrators | `duo_administrators_delete_activation_link_to_administrator_pending_activation` | Delete Activation Link to Administrator Pending Activation. | DELETE /admin/v1/admins/[admin_id]/activation_link | admin_id(必填) |
| administrators | `duo_administrators_delete_administrator` | Delete Administrator. | DELETE /admin/v1/admins/[admin_id] | admin_id(必填) |
| administrators | `duo_administrators_delete_pending_administrator_activation` | Delete Pending Administrator Activation. | DELETE /admin/v1/admins/activations/[admin_activation_id] | admin_activation_id(必填) |
| administrators | `duo_administrators_email_activation_link_to_administrator_pending_activation` | Email Activation Link to Administrator Pending Activation. | POST /admin/v1/admins/[admin_id]/activation_link/email | admin_id(必填) |
| administrators | `duo_administrators_modify_admin_external_password_management_status_or_password` | Modify Admin External Password Management Status or Password. | POST /admin/v1/admins/[admin_id]/password_mgmt | admin_id(必填), has_external_password_mgmt(可选), password(可选) |
| administrators | `duo_administrators_modify_administrator` | Modify Administrator. | POST /admin/v1/admins/[admin_id] | admin_id(必填), name(可选), phone(可选), password_change_required(可选), role(可选), restricted_by_admin_units(可选), status(可选), token_id(可选) |
| administrators | `duo_administrators_reset_administrator_authentication_attempts` | Reset Administrator Authentication Attempts. | POST /admin/v1/admins/[admin_id]/reset | admin_id(必填) |
| administrators | `duo_administrators_restrict_administrator_authentication_factors` | Restrict Administrator Authentication Factors. | POST /admin/v1/admins/allowed_auth_methods | hardware_token_enabled(可选), mobile_otp_enabled(可选), push_enabled(可选), sms_enabled(可选), voice_enabled(可选), yubikey_enabled(可选) |
| administrators | `duo_administrators_retrieve_admin_external_password_management_status` | Retrieve Admin External Password Management Status. | GET /admin/v1/admins/password_mgmt | limit(可选), offset(可选) |
| administrators | `duo_administrators_retrieve_admin_external_password_management_status_by_id` | Retrieve Admin External Password Management Status by ID. | GET /admin/v1/admins/[admin_id]/password_mgmt | admin_id(必填) |
| administrators | `duo_administrators_retrieve_administrator_authentication_factors` | Retrieve Administrator Authentication Factors. | GET /admin/v1/admins/allowed_auth_methods | 无 |
| administrators | `duo_administrators_retrieve_administrator_by_id` | Retrieve Administrator by ID. | GET /admin/v1/admins/[admin_id] | admin_id(必填) |
| administrators | `duo_administrators_retrieve_administrators` | Retrieve Administrators. | GET /admin/v1/admins | limit(可选), offset(可选) |
| administrators | `duo_administrators_retrieve_pending_administrator_activation` | Retrieve Pending Administrator Activation. | GET /admin/v1/admins/activations | limit(可选), offset(可选) |
| administrators | `duo_administrators_sync_admin_from_directory` | Sync Admin from directory. | POST /admin/v1/admins/directorysync/{directory_key}/syncadmin | directory_key(必填), email(必填) |
| bulk_operations | `duo_bulk_operations_bulk_user_operations` | Bulk User Operations. | POST /admin/v1/bulk | body(必填) |
| bypass_codes | `duo_bypass_codes_create_bypass_codes_for_user` | Create Bypass Codes for User. | POST /admin/v1/users/{user_id}/bypass_codes | user_id(必填), count(可选), codes(可选), reuse_count(可选), valid_secs(可选) |
| bypass_codes | `duo_bypass_codes_delete_bypass_code` | Delete Bypass Code. | DELETE /admin/v1/bypass_codes/[bypass_code_id] | bypass_code_id(必填) |
| bypass_codes | `duo_bypass_codes_retrieve_bypass_codes_by_id` | Retrieve Bypass Codes by ID. | GET /admin/v1/bypass_codes/{bypass_code_id} | bypass_code_id(必填) |
| bypass_codes | `duo_bypass_codes_retrieve_bypass_codes_by_user_id` | Retrieve Bypass Codes by User ID. | GET /admin/v1/users/[user_id]/bypass_codes | user_id(必填), limit(可选), offset(可选) |
| bypass_codes | `duo_bypass_codes_retrive_bypass_codes` | Retrive Bypass Codes. | GET /admin/v1/bypass_codes | limit(可选), offset(可选) |
| custom_branding | `duo_custom_branding_add_draft_custom_branding_user_by_id` | Add Draft Custom Branding User by ID. | POST /admin/v1/branding/draft/users/{user_id} | user_id(必填) |
| custom_branding | `duo_custom_branding_modify_custom_messaging` | Modify Custom Messaging. | POST /admin/v1/branding/custom_messaging | 无 |
| custom_branding | `duo_custom_branding_modify_draft_custom_branding` | Modify Draft Custom Branding. | POST /admin/v1/branding/draft | 无 |
| custom_branding | `duo_custom_branding_modify_live_custom_branding` | Modify Live Custom Branding. | POST /admin/v1/branding | 无 |
| custom_branding | `duo_custom_branding_publish_draft_custom_branding` | Publish Draft Custom Branding. | POST /admin/v1/branding/draft/publish | 无 |
| custom_branding | `duo_custom_branding_retrieve_custom_messaging` | Retrieve Custom Messaging. | GET /admin/v1/branding/custom_messaging | 无 |
| custom_branding | `duo_custom_branding_retrieve_draft_custom_branding` | Retrieve Draft Custom Branding. | GET /admin/v1/branding/draft | 无 |
| custom_branding | `duo_custom_branding_retrieve_live_custom_branding` | Retrieve Live Custom Branding. | GET /admin/v1/branding | 无 |
| desktop_authenticators | `duo_desktop_authenticators_create_shared_device_authentication_configuration` | Create Shared Device Authentication Configuration. | POST /admin/v1/desktop_authenticators/shared_device_auth | body(必填) |
| desktop_authenticators | `duo_desktop_authenticators_delete_desktop_authenticator` | Delete Desktop Authenticator. | DELETE /admin/v1/desktop_authenticators/{dakey} | dakey(必填) |
| desktop_authenticators | `duo_desktop_authenticators_retrieve_desktop_authenticator_by_id` | Retrieve Desktop Authenticator by ID. | GET /admin/v1/desktop_authenticators/{dakey} | dakey(必填) |
| desktop_authenticators | `duo_desktop_authenticators_retrieve_desktop_authenticators` | Retrieve Desktop Authenticators. | GET /admin/v1/desktop_authenticators | limit(可选), offset(可选) |
| desktop_authenticators | `duo_desktop_authenticators_retrieve_shared_device_authentication_configuration_by_key` | Retrieve Shared Device Authentication Configuration by Key. | GET /admin/v1/desktop_authenticators/shared_device_auth/{shared_device_key} | shared_device_key(必填) |
| desktop_authenticators | `duo_desktop_authenticators_retrieve_shared_device_authentication_configurations` | Retrieve Shared Device Authentication Configurations. | GET /admin/v1/desktop_authenticators/shared_device_auth | limit(可选), offset(可选) |
| desktop_authenticators | `duo_desktop_authenticators_update_shared_device_authentication_configuration` | Update Shared Device Authentication Configuration. | PUT /admin/v1/desktop_authenticators/shared_device_auth/{shared_device_key} | shared_device_key(必填), body(必填) |
| desktop_authenticators | `duo_desktop_authenticators_update_shared_device_authentication_configuration_copy` | Update Shared Device Authentication Configuration Copy. | DELETE /admin/v1/desktop_authenticators/shared_device_auth/{shared_device_key} | shared_device_key(必填) |
| endpoints | `duo_endpoints_retrieve_endpoints` | Retrieve Endpoints. | GET /admin/v1/endpoints | limit(可选), offset(可选) |
| endpoints | `duo_endpoints_retrieve_endpoints_by_id` | Retrieve Endpoints by ID. | GET /admin/v1/endpoints/[epkey] | epkey(必填) |
| groups | `duo_groups_associate_group_with_user` | Associate Group with User. | POST /admin/v1/users/{user_id}/groups | user_id(必填), group_id(必填) |
| groups | `duo_groups_create_group` | Create Group. | POST /admin/v1/groups | name(必填), desc(可选), status(可选) |
| groups | `duo_groups_delete_group` | Delete Group. | DELETE /admin/v1/groups/{group_id} | group_id(必填) |
| groups | `duo_groups_disassociate_group_from_user` | Disassociate Group from User. | DELETE /admin/v1/users/{user_id}/groups/{group_id} | user_id(必填), group_id(必填) |
| groups | `duo_groups_get_group_info` | Get Group Info. | GET /admin/v2/groups/{group_id} | group_id(必填) |
| groups | `duo_groups_get_group_members` | Get Group Members. | GET /admin/v2/groups/{group_id}/users | group_id(必填) |
| groups | `duo_groups_retrieve_groups` | Retrieve Groups. | GET /admin/v1/groups | limit(可选), offset(可选) |
| groups | `duo_groups_retrieve_groups_by_user_id` | Retrieve Groups by User ID. | GET /admin/v1/users/{user_id}/groups | user_id(必填), limit(可选), offset(可选) |
| groups | `duo_groups_update_group` | Update Group. | POST /admin/v1/groups/{group_id} | group_id(必填), name(可选), desc(可选), status(可选) |
| integrations | `duo_integrations_create_integration_v3` | Create Integration (v3). | POST /admin/v3/integrations | body(必填) |
| integrations | `duo_integrations_create_integrations_legacy` | Create Integrations (legacy). | POST /admin/v1/integrations | name(必填), type(必填), adminapi_admins(可选), adminapi_info(可选), adminapi_integrations(可选), adminapi_read_log(可选), adminapi_read_resource(可选), adminapi_settings(可选), adminapi_write_resource(可选), enroll_policy(可选), greeting(可选), groups_allowed(可选), ip_whitelist(可选), networks_for_api_access(可选), notes(可选), trusted_device_days(可选), self_service_allowed(可选), username_normalization_policy(可选) |
| integrations | `duo_integrations_create_sso_integration` | Create SSO Integration. | POST /admin/v2/integrations | body(必填) |
| integrations | `duo_integrations_delete_integration` | Delete Integration. | DELETE /admin/v2/integrations/{integration_key} | integration_key(必填) |
| integrations | `duo_integrations_modify_integration` | Modify Integration. | POST /admin/v2/integrations/[integration_key] | integration_key(必填), name(可选), networks_for_api_access(可选), adminapi_admins(可选), adminapi_info(可选), adminapi_integrations(可选), adminapi_read_log(可选), adminapi_read_resource(可选), adminapi_settings(可选), adminapi_write_resource(可选), trusted_device_days(可选), enroll_policy(可选), greeting(可选), groups_allowed(可选), ip_whitelist(可选), ip_whitelist_enroll_policy(可选), policy_key(可选), reset_secret_key(可选), self_service_allowed(可选), username_normalization_policy(可选) |
| integrations | `duo_integrations_modify_sso_integration` | Modify SSO Integration. | POST /admin/v2/integrations/{integration_key} | integration_key(必填), body(必填) |
| integrations | `duo_integrations_reset_oauth_client_secret` | Reset OAUTH client secret. | POST /admin/v2/integrations/oauth_cc/{integration_key}/client_secret/{client_id} | integration_key(必填), client_id(必填) |
| integrations | `duo_integrations_reset_oidc_client_secret` | Reset OIDC client secret. | POST /admin/v2/integrations/oidc/{integration_key}/client_secret | integration_key(必填) |
| integrations | `duo_integrations_retrieve_integration_by_integration_key` | Retrieve Integration by Integration Key. | GET /admin/v2/integrations/{integration_key} | integration_key(必填) |
| integrations | `duo_integrations_retrieve_integrations` | Retrieve Integrations. | GET /admin/v2/integrations | limit(可选), offset(可选) |
| integrations | `duo_integrations_retrieve_oauth_client_secret` | Retrieve OAUTH client secret. | GET /admin/v2/integrations/oauth_cc/{integration_key}/client_secret/{client_id} | integration_key(必填), client_id(必填) |
| integrations | `duo_integrations_retrieve_oidc_client_secret` | Retrieve OIDC client secret. | GET /admin/v2/integrations/oidc/{integration_key}/client_secret | integration_key(必填) |
| integrations | `duo_integrations_retrieve_secret_key` | Retrieve secret key. | GET /admin/v1/integrations/{integration_key}/skey | integration_key(必填) |
| logs | `duo_logs_activity_logs` | Activity Logs. | GET /admin/v2/logs/activity | mintime(必填), maxtime(必填), limit(可选), next_offset(可选), sort(可选) |
| logs | `duo_logs_administrator_logs` | Administrator Logs. | GET /admin/v1/logs/administrator | mintime(可选) |
| logs | `duo_logs_authentication_logs` | Authentication Logs. | GET /admin/v2/logs/authentication | mintime(必填), maxtime(必填), limit(可选), next_offset(可选), sort(可选), applications(可选), users(可选), event_types(可选), factors(可选), groups(可选), phone_numbers(可选), reasons(可选), results(可选), registration_id(可选), token_id(可选), webauthnkey(可选) |
| logs | `duo_logs_authentication_logs_legacy_v1` | Authentication Logs (Legacy v1). | GET /admin/v1/logs/authentication | mintime(可选) |
| logs | `duo_logs_offline_enrollment_logs` | Offline Enrollment Logs. | GET /admin/v1/logs/offline_enrollment | mintime(可选) |
| logs | `duo_logs_telephony_logs` | Telephony Logs. | GET /admin/v1/logs/telephony | mintime(可选) |
| logs | `duo_logs_telephony_logs_v2` | Telephony Logs (v2). | GET /admin/v2/logs/telephony | mintime(必填), maxtime(必填) |
| passport | `duo_passport_get_configuration` | Get Configuration. | GET /admin/v2/passport/config | 无 |
| passport | `duo_passport_modify_configuration` | Modify Configuration. | POST /admin/v2/passport/config | body(必填) |
| phones | `duo_phones_associate_phone_with_user` | Associate Phone with User. | POST /admin/v1/users/{user_id}/phones | user_id(必填), phone_id(必填) |
| phones | `duo_phones_create_activation_code` | Create Activation Code. | POST /admin/v1/phones/{phone_id}/activation_url | phone_id(必填), valid_secs(可选), install(可选) |
| phones | `duo_phones_create_activation_code_via_sms` | Create Activation Code via SMS. | POST /admin/v1/phones/{phone_id}/send_sms_activation | phone_id(必填), valid_secs(可选), install(可选), installation_msg(可选), activation_msg(可选) |
| phones | `duo_phones_create_phone` | Create Phone. | POST /admin/v1/phones | 无 |
| phones | `duo_phones_delete_phone` | Delete Phone. | DELETE /admin/v1/phones/{phone_id} | phone_id(必填) |
| phones | `duo_phones_disassociate_phone_from_user` | Disassociate Phone from User. | DELETE /admin/v1/users/{user_id}/phones/{phone_id} | user_id(必填), phone_id(必填) |
| phones | `duo_phones_modify_phone` | Modify Phone. | POST /admin/v1/phones/{phone_id} | phone_id(必填), number(可选), name(可选), extension(可选), type(可选), platform(可选), predelay(可选), postdelay(可选) |
| phones | `duo_phones_retrieve_phone_by_id` | Retrieve Phone by ID. | GET /admin/v1/phones/{phone_id} | phone_id(必填) |
| phones | `duo_phones_retrieve_phones` | Retrieve Phones. | GET /admin/v1/phones | number(可选), extension(可选), limit(可选), offset(可选) |
| phones | `duo_phones_retrieve_phones_by_user_id` | Retrieve Phones by User ID. | GET /admin/v1/users/{user_id}/phones | user_id(必填), limit(可选), offset(可选) |
| phones | `duo_phones_send_installation_url_via_sms` | Send Installation URL via SMS. | POST /admin/v1/phones/{phone_id}/send_sms_installation | phone_id(必填), installation_msg(可选) |
| phones | `duo_phones_send_passcodes_via_sms` | Send Passcodes via SMS. | POST /admin/v1/phones/{phone_id}/send_sms_passcodes | phone_id(必填) |
| policies | `duo_policies_add_new_policy_post` | Add new policy. | POST /admin/v2/policies | body(必填) |
| policies | `duo_policies_add_new_policy_post_policies` | Add new policy. | POST /admin/v2/policies | body(必填) |
| policies | `duo_policies_copy_policy` | Copy Policy. | POST /admin/v2/policies/copy | body(必填) |
| policies | `duo_policies_delete_policy` | Delete policy. | DELETE /admin/v2/policies/{policy_key} | policy_key(必填) |
| policies | `duo_policies_get_all_policies` | Get all policies. | GET /admin/v2/policies | 无 |
| policies | `duo_policies_get_policy_by_id` | Get policy by ID. | GET /admin/v2/policies/{policy_key} | policy_key(必填) |
| policies | `duo_policies_resulting_policy` | Resulting policy. | GET /admin/v2/policies/calculate | user_id(必填), integration_key(必填) |
| policies | `duo_policies_summarize_policies` | Summarize Policies. | GET /admin/v2/policies/summary | 无 |
| policies | `duo_policies_update_policy` | Update policy. | PUT /admin/v2/policies/{policy_key} | policy_key(必填), body(必填) |
| policies | `duo_policies_update_policy_deny_new_users` | Update policy deny new users. | PUT /admin/v2/policies/{policy_key} | policy_key(必填), body(必填) |
| registered_devices | `duo_registered_devices_block_device_by_id` | Block Device by ID. | POST /admin/v1/registered_devices/blocked/{compkey} | compkey(必填) |
| registered_devices | `duo_registered_devices_block_devices` | Block Devices. | POST /admin/v1/registered_devices/blocked | body(必填) |
| registered_devices | `duo_registered_devices_delete_registered_device` | Delete Registered Device. | DELETE /admin/v1/registered_devices/{registered_device_key} | registered_device_key(必填) |
| registered_devices | `duo_registered_devices_retrieve_blocked_devices` | Retrieve Blocked Devices. | GET /admin/v1/registered_devices/blocked | 无 |
| registered_devices | `duo_registered_devices_retrieve_blocked_devices_by_id` | Retrieve Blocked Devices by ID. | GET /admin/v1/registered_devices/blocked/{compkey} | compkey(必填) |
| registered_devices | `duo_registered_devices_retrieve_registered_device_by_id` | Retrieve Registered Device by ID. | GET /admin/v1/registered_devices/{registered_device_key} | registered_device_key(必填) |
| registered_devices | `duo_registered_devices_retrieve_registered_devices` | Retrieve Registered Devices. | GET /admin/v1/registered_devices | 无 |
| registered_devices | `duo_registered_devices_unblock_device_by_id` | Unblock Device by ID. | DELETE /admin/v1/registered_devices/blocked/{compkey} | compkey(必填) |
| registered_devices | `duo_registered_devices_unblock_devices` | Unblock Devices. | DELETE /admin/v1/registered_devices/blocked | body(必填) |
| settings | `duo_settings_delete_duo_mobile_logo` | Delete Duo Mobile Logo. | DELETE /admin/v1/logo | 无 |
| settings | `duo_settings_modify_duo_mobile_logo` | Modify Duo Mobile Logo. | POST /admin/v1/logo | 无 |
| settings | `duo_settings_modify_settings` | Modify Settings. | POST /admin/v1/settings | caller_id(可选), fraud_email(可选), fraud_email_enabled(可选), inactive_user_expiration(可选), keypress_confirm(可选), keypress_fraud(可选), language(可选), lockout_expire_duration(可选), lockout_threshold(可选), minimum_password_length(可选), mobile_otp_enabled(可选), password_requires_lower_alpha(可选), password_requires_numeric(可选), password_requires_special(可选), password_requires_upper_alpha(可选), push_enabled(可选), sms_batch(可选), sms_enabled(可选), sms_expiration(可选), sms_message(可选), sms_refresh(可选), telephony_warning_min(可选), timezone(可选), voice_enabled(可选), user_telephony_cost_max(可选), u2f_enabled(可选) |
| settings | `duo_settings_retrieve_duo_mobile_logo` | Retrieve Duo Mobile Logo. | GET /admin/v1/logo | 无 |
| settings | `duo_settings_retrieve_settings` | Retrieve Settings. | GET /admin/v1/settings | 无 |
| tokens | `duo_tokens_create_hardware_token` | Create Hardware Token. | POST /admin/v1/tokens | type(必填), serial(必填), secret(可选), counter(可选), private_id(可选), aes_key(可选) |
| tokens | `duo_tokens_delete_hardware_token` | Delete Hardware Token. | DELETE /admin/v1/tokens/{token_id} | token_id(必填) |
| tokens | `duo_tokens_resync_hardware_token` | Resync Hardware Token. | POST /admin/v1/tokens/{token_id}/resync | token_id(必填), code1(必填), code2(必填), code3(必填) |
| tokens | `duo_tokens_retrieve_hardware_token_by_id` | Retrieve Hardware Token by ID. | GET /admin/v1/tokens/{token_id} | token_id(必填) |
| tokens | `duo_tokens_retrieve_hardware_tokens` | Retrieve Hardware Tokens. | GET /admin/v1/tokens | type(可选), serial(可选), limit(可选), offset(可选) |
| trust_monitor | `duo_trust_monitor_retrieve_events` | Retrieve Events. | GET /admin/v1/trust_monitor/events | mintime(必填), maxtime(必填), limit(可选), offset(可选), type(可选) |
| users | `duo_users_associate_group_with_user` | Associate Group with User. | POST /admin/v1/users/{user_id}/groups | user_id(必填), group_id(必填) |
| users | `duo_users_associate_hardware_token_with_user` | Associate Hardware Token with User. | POST /admin/v1/users/{user_id}/tokens | user_id(必填), token_id(必填) |
| users | `duo_users_associate_phone_with_user` | Associate Phone with User. | POST /admin/v1/users/{user_id}/phones | user_id(必填), phone_id(必填) |
| users | `duo_users_bulk_add_users` | Bulk Add Users. | POST /admin/v1/users/bulk_create | body(必填) |
| users | `duo_users_bulk_restore_users_from_trash` | Bulk Restore Users from Trash. | POST /admin/v1/users/bulk_restore | body(必填) |
| users | `duo_users_create_bypass_codes_for_user` | Create Bypass Codes for User. | POST /admin/v1/users/{user_id}/bypass_codes | user_id(必填), count(可选), codes(可选), reuse_count(可选), valid_secs(可选) |
| users | `duo_users_create_user` | Create User. | POST /admin/v1/users | username(必填), aliases(可选), realname(可选), email(可选), status(可选), notes(可选), firstname(可选), lastname(可选) |
| users | `duo_users_delete_user` | Delete User. | DELETE /admin/v1/users/{user_id} | user_id(必填) |
| users | `duo_users_disassocate_hardware_token_from_user` | Disassocate Hardware Token from User. | DELETE /admin/v1/users/{user_id}/tokens/{token_id} | user_id(必填), token_id(必填) |
| users | `duo_users_disassociate_group_from_user` | Disassociate Group from User. | DELETE /admin/v1/users/{user_id}/groups/{group_id} | user_id(必填), group_id(必填) |
| users | `duo_users_disassociate_phone_from_user` | Disassociate Phone from User. | DELETE /admin/v1/users/{user_id}/phones/{phone_id} | user_id(必填), phone_id(必填) |
| users | `duo_users_enroll_user` | Enroll User. | POST /admin/v1/users/enroll | username(必填), email(必填), valid_secs(可选) |
| users | `duo_users_modify_user` | Modify User. | POST /admin/v1/users/{user_id} | user_id(必填), username(可选), aliases(可选), realname(可选), email(可选), status(可选), notes(可选), firstname(可选), lastname(可选) |
| users | `duo_users_retrieve_bypass_codes_by_user_id` | Retrieve Bypass Codes by User ID. | GET /admin/v1/users/{user_id}/bypass_codes | user_id(必填), limit(可选), offset(可选) |
| users | `duo_users_retrieve_desktop_authenticators_by_user_id` | Retrieve Desktop Authenticators by User ID. | GET /admin/v1/users/{user_id}/desktopauthenticators | user_id(必填) |
| users | `duo_users_retrieve_groups_by_user_id` | Retrieve Groups by User ID. | GET /admin/v1/users/{user_id}/groups | user_id(必填), limit(可选), offset(可选) |
| users | `duo_users_retrieve_hardware_tokens_by_user_id` | Retrieve Hardware Tokens by User ID. | GET /admin/v1/users/{user_id}/tokens | user_id(必填), limit(可选), offset(可选) |
| users | `duo_users_retrieve_phones_by_user_id` | Retrieve Phones by User ID. | GET /admin/v1/users/{user_id}/phones | user_id(必填), limit(可选), offset(可选) |
| users | `duo_users_retrieve_user_by_id` | Retrieve User by ID. | GET /admin/v1/users/{user_id} | user_id(必填) |
| users | `duo_users_retrieve_users` | Retrieve Users. | GET /admin/v1/users | username(可选), limit(可选), offset(可选) |
| users | `duo_users_retrieve_verification_push_response` | Retrieve Verification Push Response. | GET /admin/v1/users/{user_id}/verification_push_response | user_id(必填), push_id(必填) |
| users | `duo_users_retrieve_web_authn_credentials_by_user_id` | Retrieve WebAuthn Credentials by User ID. | GET /admin/v1/users/{user_id}/webauthncredentials | user_id(必填) |
| users | `duo_users_send_multiple_users_to_trash` | Send Multiple Users to Trash. | POST /admin/v1/users/bulk_send_to_trash | body(必填) |
| users | `duo_users_send_verification_push` | Send Verification Push. | POST /admin/v1/users/{user_id}/send_verification_push | user_id(必填), body(必填) |
| users | `duo_users_synchronize_user_from_directory` | Synchronize User from Directory. | POST /admin/v1/users/directorysync/{directory_key}/syncuser | directory_key(必填), username(必填) |
| webauthn_credentials | `duo_webauthn_credentials_delete_web_authn_credential` | Delete WebAuthn Credential. | DELETE /admin/v1/webauthncredentials/[webauthnkey] | webauthnkey(必填) |
| webauthn_credentials | `duo_webauthn_credentials_retrieve_web_authn_credentials` | Retrieve WebAuthn Credentials. | GET /admin/v1/webauthncredentials | limit(可选), offset(可选) |
| webauthn_credentials | `duo_webauthn_credentials_retrieve_web_authn_credentials_by_key` | Retrieve WebAuthn Credentials by Key. | GET /admin/v1/webauthncredentials/[webauthnkey] | webauthnkey(必填) |
| webauthn_credentials | `duo_webauthn_credentials_retrieve_web_authn_credentials_by_user_id` | Retrieve WebAuthn Credentials by User ID. | GET /admin/v1/users/[user_id]/webauthncredentials | user_id(必填) |

## 测试示例

```bash
# Health check
curl -s http://localhost:8080/health

# Call a tool via the MCP protocol (streamable HTTP) — requires an
# initialize handshake first per the MCP spec; abbreviated example below
# shows the tool-call request body only:
curl -s -X POST http://localhost:8080/mcp \
  -H "X-Duo-Ikey: <your-integration-key>" \
  -H "X-Duo-Skey: <your-secret-key>" \
  -H "X-Duo-Api-Host: api-xxxxxxxx.duosecurity.com" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: <session-id-from-initialize>" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "duo_users_retrieve_users",
      "arguments": {"limit": "5"}
    }
  }'
```

**Signing correctness verified independently of any live account**: this
server's HMAC-SHA512 request-signing implementation was directly compared,
side-by-side in the same Python process, against Duo's own official
reference client (`duo_client_python`) — the canonical string, the full
`Authorization: Basic` header, and percent-encoding of special characters
were all confirmed byte-for-byte identical for both a GET (query-signed) and
a POST (JSON-body-signed) scenario. Structural checks were also completed:
MCP handshake, `tools/list` returning all 160 registered tools, and 401
credential-gating with placeholder header values.

**Live self-test against a real Duo account: passed.** Using a real Admin API
integration created in a live Duo account, three calls were made through the
running MCP server end-to-end (real HTTP requests to
`api-4d02a5dd.duosecurity.com`, real HMAC-SHA512 signing, real response
parsing):

- `duo_administrators_retrieve_administrators` → returned the real account
  owner (`ryan.li@mspbots.ai`, role `Owner`, an enrolled iPhone with push
  capability).
- `duo_integrations_retrieve_integrations` → returned the Admin API
  integration itself, with `integration_key` matching the ikey used to
  authenticate — direct proof the signature was accepted by Duo.
- `duo_users_retrieve_users` → returned `[]`. Cross-checked against the two
  calls above (not assumed): since both other calls returned real,
  non-empty data through the identical auth/parsing path, the empty array
  reflects a genuinely fresh account with zero enrolled end users yet, not
  a masked auth failure.

## API Reference

- Admin API docs: https://duo.com/docs/adminapi
- Official Postman collection: https://github.com/duosecurity/duo_postman_collection
- Reference Python client (signing algorithm source): https://github.com/duosecurity/duo_client_python

## Known Gaps

- **Full API coverage was an explicit user decision** after confirming no
  official/community Duo Admin API MCP exists and no MSPbots-existing
  integration could anchor a narrower scope. Every `Create`/`Modify`/
  `Delete`/`Bulk` tool mutates real Duo account configuration (users,
  groups, phones, tokens, integrations, policies, administrators, custom
  branding, etc.) — treat these as destructive/irreversible and confirm
  with a human before invoking, especially anything under `administrators`
  (could lock out real admin accounts) or `integrations`/`policies`
  (could break production SSO/access policies).
- **`body` parameters are untyped (`dict`)** for the ~20 endpoints with
  nested/complex JSON payloads (bulk operations, SSO integration config,
  policy sections, shared-device-auth config) — each tool's docstring lists
  the top-level keys from Duo's own example payload; the full schema is in
  the linked API reference.
- **Live functional self-test passed** against a real Duo account (see
  Self-Test section above) — administrators and integrations endpoints
  returned real data; the users endpoint correctly returned an empty list
  for this account's current (zero end-user) state.
- Duo's own official Postman collection has two small authoring
  inconsistencies, both worked around here: (1) some path placeholders use
  `[bracket]` notation instead of Postman's `{{double-brace}}` variables —
  both styles are recognized; (2) two operations (`Create Integrations
  (legacy)`, `Modify Integration`) list the same query parameter twice
  under one operation — deduplicated, keeping the first occurrence. One
  operation (`Remove Draft Custom Branding User by ID`) has a malformed
  `request` object with no `url` at all in the source collection and was
  skipped entirely (160 usable tools + this 1 skipped = the source
  collection's nominal 161 total).
