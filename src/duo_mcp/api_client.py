import asyncio
import base64
import email.utils
import hashlib
import hmac
import json
from typing import Any
from urllib.parse import quote, urlencode

import httpx

from ._json import error_envelope

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

_TIMEOUT = httpx.Timeout(connect=5.0, read=30.0, write=10.0, pool=5.0)
_RETRYABLE_STATUS = {429, 500, 502, 503, 504}
_MAX_RETRIES = 3
_MAX_BACKOFF_SECONDS = 20.0

# One shared connection pool for the process lifetime. It carries no auth
# state of its own — ikey/skey are only ever read, per request, inside
# DuoClient.request() to compute a fresh Authorization header — so sharing
# it across concurrent tenants is safe (see server.py's contextvar-based
# credential isolation, which is what actually keeps tenants apart).
_http_client: httpx.AsyncClient | None = None


def _get_http_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None:
        _http_client = httpx.AsyncClient(timeout=_TIMEOUT, follow_redirects=True)
    return _http_client


# status_code -> (error code, retryable). status_code 0 means a network/
# connection-level failure (no response at all).
_STATUS_TO_CODE: dict[int, tuple[str, bool]] = {
    0: ("upstream_error", True),
    400: ("invalid_argument", False),
    401: ("unauthorized", False),
    403: ("unauthorized", False),
    404: ("not_found", False),
    422: ("invalid_argument", False),
    429: ("rate_limited", True),
}


def _classify(status_code: int) -> tuple[str, bool]:
    if status_code in _STATUS_TO_CODE:
        return _STATUS_TO_CODE[status_code]
    if status_code >= 500:
        return "upstream_error", True
    return "invalid_argument", False


class DuoError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Duo API error {status_code}: {message}")

    def to_envelope(self) -> str:
        code, retryable = _classify(self.status_code)
        return error_envelope(code, self.message, retryable)


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
    as every other tool in this server. Uses the shared module-level
    connection pool (see _get_http_client) rather than opening a new
    connection per request.
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
        """Sign and send a single Duo Admin API request, with limited retry.

        `params` becomes a signed, url-encoded query string for GET/DELETE,
        or the entire signed JSON request body for POST/PUT/PATCH — exactly
        matching the reference client's behavior. Callers never need to pick
        which transport a given param uses; the HTTP method decides it.

        Retries on 429/5xx (respecting Retry-After, capped exponential
        backoff, 3 attempts max) re-sign from scratch on every attempt: the
        canonical string that gets HMAC-signed includes the `Date` header,
        so naively reusing the first attempt's Authorization header on a
        retry would carry a stale timestamp and Duo would reject it with a
        401. Each loop iteration below generates a fresh `date` and calls
        `_sign` again, so every attempt is independently valid.
        """
        method = method.upper()
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}
        params_go_in_body = method in _METHODS_WITH_BODY_PARAMS
        client = _get_http_client()

        last_exc: Exception | None = None
        for attempt in range(_MAX_RETRIES + 1):
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

            url = f"https://{self._host}{request_path}"
            try:
                resp = await client.request(
                    method,
                    url,
                    headers=headers,
                    content=body if params_go_in_body else None,
                )
            except httpx.RequestError as e:
                last_exc = e
                if attempt < _MAX_RETRIES:
                    await asyncio.sleep(min(2**attempt, _MAX_BACKOFF_SECONDS))
                    continue
                raise DuoError(0, f"{e or type(e).__name__}") from e

            if resp.status_code in _RETRYABLE_STATUS and attempt < _MAX_RETRIES:
                await asyncio.sleep(self._retry_delay(resp, attempt))
                continue

            return self._parse(resp)

        # Unreachable in practice (loop always returns or raises above), but
        # keeps type checkers happy and guards against future edits.
        if last_exc:
            raise DuoError(0, f"{last_exc}") from last_exc
        raise DuoError(0, "request failed with no response")

    def _retry_delay(self, resp: httpx.Response, attempt: int) -> float:
        retry_after = resp.headers.get("Retry-After")
        if retry_after:
            try:
                return min(float(retry_after), _MAX_BACKOFF_SECONDS)
            except ValueError:
                pass
        return min(2**attempt, _MAX_BACKOFF_SECONDS)

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
