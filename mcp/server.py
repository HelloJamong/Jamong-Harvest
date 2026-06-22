#!/usr/bin/env python3
import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

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
    mcp.run(transport="sse", host="0.0.0.0", port=port)
