import contextvars
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from .api_client import DuoClient
from .config import Settings

# Per-request credential isolation via contextvars.
# GatewayTokenMiddleware sets this before the MCP handler runs.
# Python asyncio copies context per task, so concurrent SSE connections are isolated.
_gateway_creds_var: contextvars.ContextVar[tuple[str, str, str] | None] = contextvars.ContextVar(
    "duo_gateway_creds", default=None
)


def get_client_from_context() -> DuoClient | None:
    """Resolve the active DuoClient for the current request context."""
    creds = _gateway_creds_var.get()
    if not creds:
        return None
    ikey, skey, host = creds
    return DuoClient(ikey, skey, host)


class GatewayTokenMiddleware:
    """ASGI middleware.

    Reads X-Duo-Ikey, X-Duo-Skey, and X-Duo-Api-Host (all required) from
    request headers and stores them in the contextvar. Returns 401 if any is
    missing on /mcp requests.
    """

    def __init__(self, app: ASGIApp, settings: Settings):
        self.app = app
        self.settings = settings

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")
        if not path.startswith("/mcp"):
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        ikey = request.headers.get("x-duo-ikey")
        skey = request.headers.get("x-duo-skey")
        api_host = request.headers.get("x-duo-api-host")
        if not ikey or not skey or not api_host:
            response = JSONResponse(
                {
                    "error": "Missing credentials",
                    "message": (
                        "This server requires the X-Duo-Ikey, X-Duo-Skey, and "
                        "X-Duo-Api-Host headers"
                    ),
                    "required_headers": ["X-Duo-Ikey", "X-Duo-Skey", "X-Duo-Api-Host"],
                    "optional_headers": [],
                },
                status_code=401,
            )
            await response(scope, receive, send)
            return

        ctx_token = _gateway_creds_var.set((ikey, skey, api_host))
        try:
            await self.app(scope, receive, send)
        finally:
            _gateway_creds_var.reset(ctx_token)


def create_mcp_server(settings: Settings) -> FastMCP:
    """Build the FastMCP server instance and register all Duo tools."""
    # DNS-rebinding protection is a browser-oriented safeguard that rejects
    # non-localhost Host headers with 421. Disable it so the server works
    # correctly behind a reverse proxy or docker network.
    mcp = FastMCP(
        name="duo-mcp",
        transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
    )

    client_factory: Callable[[], DuoClient | None] = get_client_from_context

    from .tools import (
        groups,
        phones,
        tokens,
        users,
        webauthn_credentials,
    )

    for mod in (
        groups,
        phones,
        tokens,
        users,
        webauthn_credentials,
    ):
        mod.register(mcp, client_factory)

    return mcp
