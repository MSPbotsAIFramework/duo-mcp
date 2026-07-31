import base64
import email.utils
import hashlib
import hmac
import json
from typing import Any
from urllib.parse import quote, urlencode

import httpx

# Duo Admin API request signing (sig_version 5), ported directly from the
# official duo_client_python reference implementation
# (https://github.com/duosecurity/duo_client_python/blob/master/duo_client/client.py)
# to guarantee byte-for-byte compatibility with Duo's server-side signature
# verification — this is HMAC signing, so any deviation (quoting, key
# ordering, hash of the wrong body) produces a silent 401 with no useful
# diagnostic, not a helpful validation error.

_EMPTY_HEADERS_HASH = hashlib.sha512(b"").hexdigest()

# Only POST/PUT/PATCH carry their params as a JSON request body; GET/DELETE
# send them as a signed, url-encoded query string. This matches the
# reference client's `params_go_in_body` rule exactly.
_METHODS_WITH_BODY_PARAMS = ("POST", "PUT", "PATCH")


class DuoError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"Duo API error {status_code}: {message}")


def _canon_params(params: dict[str, Any]) -> str:
    """Canonical query-string form of params, per Duo's OAuth1.0-style
    percent-encoding (safe='~') and lexicographic (key, value) sort."""
    pairs = []
    for key, value in (params or {}).items():
        if value is None:
            continue
        pairs.append((quote(str(key), safe="~"), quote(str(value), safe="~")))
    pairs.sort()
    return "&".join(f"{k}={v}" for k, v in pairs)


def _canon_json(params: dict[str, Any]) -> str:
    return json.dumps(params, sort_keys=True, separators=(",", ":"))


class DuoClient:
    """Async httpx client wrapping the Cisco Duo Admin API (sig_version 5).

    Auth is per-request HMAC-SHA512 request signing with an integration key
    (ikey) and secret key (skey) — never a simple bearer token. Credentials
    are held only for the lifetime of a single request/response cycle, same
    as every other tool in this server.
    """

    def __init__(self, ikey: str, skey: str, host: str):
        self._ikey = ikey
        self._skey = skey
        host = host.strip()
        for prefix in ("https://", "http://"):
            if host.startswith(prefix):
                host = host[len(prefix) :]
        self._host = host.rstrip("/")

    def _sign(self, method: str, path: str, sig_params: dict, body: str, date: str) -> str:
        canonical = "\n".join(
            [
                date,
                method.upper(),
                self._host.lower(),
                path,
                _canon_params(sig_params),
                hashlib.sha512(body.encode("utf-8")).hexdigest(),
                _EMPTY_HEADERS_HASH,
            ]
        )
        digest = hmac.new(
            self._skey.encode("utf-8"), canonical.encode("utf-8"), hashlib.sha512
        )
        auth = f"{self._ikey}:{digest.hexdigest()}"
        return "Basic " + base64.b64encode(auth.encode("utf-8")).decode("utf-8")

    async def request(self, method: str, path: str, params: dict[str, Any] | None = None) -> Any:
        """Sign and send a single Duo Admin API request.

        `params` becomes a signed, url-encoded query string for GET/DELETE,
        or the entire signed JSON request body for POST/PUT/PATCH — exactly
        matching the reference client's behavior. Callers never need to
        pick which transport a given param uses; the HTTP method decides it.
        """
        method = method.upper()
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}
        params_go_in_body = method in _METHODS_WITH_BODY_PARAMS
        date = email.utils.formatdate()  # RFC 2822, UTC ("-0000" offset)

        if params_go_in_body:
            body = _canon_json(clean_params)
            sig_params: dict[str, Any] = {}
            request_path = path
        else:
            body = ""
            sig_params = clean_params
            query = urlencode(clean_params)
            request_path = f"{path}?{query}" if query else path

        auth_header = self._sign(method, path, sig_params, body, date)
        headers = {
            "Authorization": auth_header,
            "Date": date,
            "User-Agent": "mspbots-duo-mcp/0.1",
        }
        if params_go_in_body:
            headers["Content-Type"] = "application/json"

        async with httpx.AsyncClient(timeout=30.0, base_url=f"https://{self._host}") as client:
            try:
                resp = await client.request(
                    method,
                    request_path,
                    headers=headers,
                    content=body if params_go_in_body else None,
                )
            except httpx.RequestError as e:
                raise DuoError(0, f"{e or type(e).__name__}") from e
            return self._parse(resp)

    def _parse(self, resp: httpx.Response) -> Any:
        try:
            data = resp.json()
        except ValueError:
            data = None

        if resp.status_code != 200 or (isinstance(data, dict) and data.get("stat") == "FAIL"):
            if isinstance(data, dict):
                msg = data.get("message") or str(data)
                detail = data.get("message_detail")
                if detail:
                    msg = f"{msg} ({detail})"
            else:
                msg = resp.text
            raise DuoError(resp.status_code, str(msg))

        if isinstance(data, dict) and "response" in data:
            return data["response"]
        return data
