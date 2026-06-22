#!/usr/bin/env python3
import os
import uvicorn
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

SKILLS_DIR = Path(__file__).parent.parent / "skills"

mcp = FastMCP("jamong-skills")


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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp_host = os.environ.get("MCP_HOST", "localhost")
    # MCP_HOST를 allowed_hosts에 등록해 DNS rebinding 보호는 유지하면서 리버스 프록시 허용
    mcp.settings.transport_security = TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=[mcp_host],
    )
    mcp.settings.host = mcp_host
    mcp.settings.port = port
    uvicorn.run(mcp.streamable_http_app(), host="0.0.0.0", port=port)
