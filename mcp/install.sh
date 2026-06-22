#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "==> Python 가상환경 생성"
python3.11 -m venv "$REPO_DIR/venv"

echo "==> Python 패키지 설치"
"$REPO_DIR/venv/bin/pip" install -r "$SCRIPT_DIR/requirements.txt"

echo ""
echo "==> systemd 서비스 등록"
SERVICE_SRC="$SCRIPT_DIR/jamong-mcp.service"
SERVICE_DST="/etc/systemd/system/jamong-mcp.service"

# 실제 경로로 치환 후 복사
REPO_DIR="$(dirname "$SCRIPT_DIR")"
sed "s|__REPO_DIR__|$REPO_DIR|g" "$SERVICE_SRC" > /tmp/jamong-mcp.service
sed -i "s|__VENV_DIR__|$REPO_DIR/venv|g" /tmp/jamong-mcp.service

echo "  아래 명령을 root로 실행하세요:"
echo ""
echo "    cp /tmp/jamong-mcp.service $SERVICE_DST"
echo "    systemctl daemon-reload"
echo "    systemctl enable --now jamong-mcp"
echo ""
echo "Done."
