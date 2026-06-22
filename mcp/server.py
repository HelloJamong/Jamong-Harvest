#!/usr/bin/env python3
import os
import secrets
import time
import uvicorn
from pathlib import Path
from pydantic import AnyHttpUrl
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, Response

from mcp.server.fastmcp import FastMCP as MCPServer
from mcp.server.auth.provider import (
    AccessToken,
    AuthorizationCode,
    AuthorizationParams,
    OAuthAuthorizationServerProvider,
    RefreshToken,
    construct_redirect_uri,
)
from mcp.server.auth.settings import AuthSettings, ClientRegistrationOptions
from mcp.server.transport_security import TransportSecuritySettings
from mcp.shared.auth import OAuthClientInformationFull, OAuthToken

SKILLS_DIR = Path(__file__).parent.parent / "skills"


class JamongOAuthProvider(OAuthAuthorizationServerProvider[AuthorizationCode, RefreshToken, AccessToken]):
    def __init__(self, server_url: str):
        self.server_url = server_url.rstrip("/")
        self.username = os.environ.get("MCP_USERNAME", "admin")
        self.password = os.environ.get("MCP_PASSWORD", "changeme")
        self.clients: dict[str, OAuthClientInformationFull] = {}
        self.auth_codes: dict[str, AuthorizationCode] = {}
        self.tokens: dict[str, AccessToken] = {}
        self.state_mapping: dict[str, dict] = {}

    async def get_client(self, client_id: str) -> OAuthClientInformationFull | None:
        return self.clients.get(client_id)

    async def register_client(self, client_info: OAuthClientInformationFull):
        if not client_info.client_id:
            raise ValueError("No client_id")
        self.clients[client_info.client_id] = client_info

    async def authorize(self, client: OAuthClientInformationFull, params: AuthorizationParams) -> str:
        state = params.state or secrets.token_hex(16)
        self.state_mapping[state] = {
            "redirect_uri": str(params.redirect_uri),
            "code_challenge": params.code_challenge,
            "redirect_uri_provided_explicitly": str(params.redirect_uri_provided_explicitly),
            "client_id": client.client_id,
            "resource": params.resource,
        }
        return f"{self.server_url}/login?state={state}"

    async def load_authorization_code(
        self, client: OAuthClientInformationFull, authorization_code: str
    ) -> AuthorizationCode | None:
        return self.auth_codes.get(authorization_code)

    async def exchange_authorization_code(
        self, client: OAuthClientInformationFull, authorization_code: AuthorizationCode
    ) -> OAuthToken:
        if authorization_code.code not in self.auth_codes:
            raise ValueError("Invalid authorization code")
        token = f"tok_{secrets.token_hex(32)}"
        self.tokens[token] = AccessToken(
            token=token,
            client_id=client.client_id,
            scopes=authorization_code.scopes,
            expires_at=int(time.time()) + 86400,
            resource=authorization_code.resource,
            subject=authorization_code.subject,
        )
        del self.auth_codes[authorization_code.code]
        return OAuthToken(
            access_token=token,
            token_type="Bearer",
            expires_in=86400,
            scope=" ".join(authorization_code.scopes),
        )

    async def load_access_token(self, token: str) -> AccessToken | None:
        t = self.tokens.get(token)
        if not t:
            return None
        if t.expires_at and t.expires_at < time.time():
            del self.tokens[token]
            return None
        return t

    async def load_refresh_token(
        self, client: OAuthClientInformationFull, refresh_token: str
    ) -> RefreshToken | None:
        return None

    async def exchange_refresh_token(self, client, refresh_token, scopes):
        raise NotImplementedError("Refresh tokens not supported")

    async def revoke_token(self, token: str, token_type_hint: str | None = None) -> None:
        self.tokens.pop(token, None)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp_host = os.environ.get("MCP_HOST", "localhost")
    server_url = os.environ.get("SERVER_URL", f"http://{mcp_host}:{port}")

    provider = JamongOAuthProvider(server_url=server_url)

    mcp = MCPServer(
        "jamong-skills",
        auth_server_provider=provider,
        auth=AuthSettings(
            issuer_url=AnyHttpUrl(server_url),
            resource_server_url=None,
            client_registration_options=ClientRegistrationOptions(
                enabled=True,
                valid_scopes=["mcp"],
                default_scopes=["mcp"],
            ),
            required_scopes=["mcp"],
        ),
    )

    @mcp.resource("skills://list")
    def list_skills() -> str:
        """사용 가능한 스킬 목록"""
        names = sorted(
            d.name for d in SKILLS_DIR.iterdir()
            if d.is_dir() and (d / "SKILL.md").exists()
        )
        return "\n".join(names)

    @mcp.resource("skill://{name}")
    def get_skill(name: str) -> str:
        """스킬 내용 반환"""
        path = SKILLS_DIR / name / "SKILL.md"
        if not path.exists():
            raise ValueError(f"Skill not found: {name}")
        return path.read_text(encoding="utf-8")

    @mcp.custom_route("/login", methods=["GET"])
    async def login_page(request: Request) -> Response:
        state = request.query_params.get("state", "")
        if not state or state not in provider.state_mapping:
            raise HTTPException(400, "Invalid or missing state")
        html = f"""<!DOCTYPE html>
<html><head><title>Jamong MCP Login</title>
<style>
  body{{font-family:sans-serif;max-width:380px;margin:80px auto;padding:20px}}
  input{{width:100%;padding:10px;margin:6px 0;box-sizing:border-box;border:1px solid #ccc;border-radius:4px}}
  button{{background:#2563eb;color:#fff;padding:10px;border:none;border-radius:4px;width:100%;cursor:pointer;margin-top:8px}}
  button:hover{{background:#1d4ed8}}
</style>
</head><body>
<h2>Jamong MCP Server</h2>
<form method="post" action="/login/callback">
  <input type="hidden" name="state" value="{state}">
  <input type="text" name="username" placeholder="Username" required autofocus>
  <input type="password" name="password" placeholder="Password" required>
  <button type="submit">Login</button>
</form>
</body></html>"""
        return HTMLResponse(html)

    @mcp.custom_route("/login/callback", methods=["POST"])
    async def login_callback(request: Request) -> Response:
        form = await request.form()
        username = str(form.get("username", ""))
        password = str(form.get("password", ""))
        state = str(form.get("state", ""))

        state_data = provider.state_mapping.get(state)
        if not state_data:
            raise HTTPException(400, "Invalid state")
        if username != provider.username or password != provider.password:
            raise HTTPException(401, "Invalid credentials")

        code = f"code_{secrets.token_hex(16)}"
        provider.auth_codes[code] = AuthorizationCode(
            code=code,
            client_id=state_data["client_id"],
            redirect_uri=AnyHttpUrl(state_data["redirect_uri"]),
            redirect_uri_provided_explicitly=state_data["redirect_uri_provided_explicitly"] == "True",
            expires_at=time.time() + 300,
            scopes=["mcp"],
            code_challenge=state_data["code_challenge"],
            resource=state_data.get("resource"),
            subject=username,
        )
        del provider.state_mapping[state]
        redirect = construct_redirect_uri(state_data["redirect_uri"], code=code, state=state)
        return RedirectResponse(url=redirect, status_code=302)

    mcp.settings.transport_security = TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=[mcp_host],
    )
    mcp.settings.host = mcp_host
    mcp.settings.port = port
    uvicorn.run(mcp.streamable_http_app(), host="0.0.0.0", port=port)
