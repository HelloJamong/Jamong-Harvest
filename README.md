# Jamong-Harvest

**AI로 키우는 개발농장** — Jamong의 AI 개발 환경에서 반복적으로 쓰이는 공통 스킬, 운영 템플릿, safety hook을 모아두는 저장소입니다.

Claude Code와 Codex에서 `install.sh` / `install.bat` 한 번으로 스킬을 설치하고, 새 프로젝트에는 템플릿을 복사해서 바로 사용합니다.

## 저장소 구조

```text
Jamong-Harvest/
├── install.sh              # Linux/macOS 스킬 설치 스크립트
├── install.bat             # Windows 스킬 설치 스크립트
├── skills/                 # Claude Code / Codex 공통 스킬
│   ├── git-workflow/
│   ├── admin-safety/
│   ├── completion-report/
│   ├── code-discipline/
│   ├── versioning/
│   └── deploy/
├── mcp/                    # MCP 서버 (스킬을 원격으로 서빙)
│   ├── server.py
│   ├── requirements.txt
│   ├── install.sh
│   └── jamong-mcp.service
├── templates/
│   ├── CLAUDE.md           # Claude Code 프로젝트 운영 템플릿
│   └── AGENTS.md           # Codex/OMX 에이전트 운영 템플릿
├── hooks/
│   ├── claude/
│   │   └── block-sudo-bash.mjs
│   └── codex/
│       └── block-sudo-bash.mjs
└── docs/
    └── guide.md            # 글로벌 환경 적용 가이드
```

## 스킬 설치

[GitHub Releases](https://github.com/HelloJamong/Jamong-Harvest/releases/latest)에서 `install.zip`을 받거나, 저장소를 직접 클론해서 실행합니다.

```bash
# Claude Code + Codex 모두 설치
./install.sh all

# Claude Code만
./install.sh claude

# Codex만
./install.sh codex
```

Windows:

```bat
install.bat all
```

### 설치 경로

| LLM | 경로 |
|-----|------|
| Claude Code | `~/.claude/skills/<skill>/SKILL.md` |
| Codex | `~/.agents/skills/<skill>/SKILL.md` |
| Codex (호환) | `~/.codex/skills/<skill>/SKILL.md` |

## 제공 스킬

| 스킬 | 트리거 상황 |
|------|------------|
| `git-workflow` | git 명령, 커밋·푸시, 브랜치 전환 시 |
| `admin-safety` | sudo/doas/pkexec 실행 시도 시 |
| `completion-report` | 작업 완료 보고 시 |
| `code-discipline` | 코드 작성 전 원칙 확인 시 |
| `versioning` | 버전 올리기, CHANGELOG 작성, tag/릴리즈 시 |
| `deploy` | Docker 이미지 빌드·배포, digest 기반 자동 업데이트 시 |

## MCP 서버

스킬을 파일로 설치하는 대신, MCP 서버에 연결해서 사용할 수 있어요. 여러 머신에서 동일한 스킬을 쓸 때 유용합니다.

### 서버 설치 (Rocky Linux / RHEL 계열)

```bash
git clone https://github.com/HelloJamong/Jamong-Harvest.git /opt/jamong-harvest
cd /opt/jamong-harvest
bash mcp/install.sh

# install.sh 안내에 따라 systemd 서비스 등록
sudo cp /tmp/jamong-mcp.service /etc/systemd/system/jamong-mcp.service
```

### MCP_HOST 설정 (필수)

서비스 파일에 외부 도메인을 직접 지정해야 합니다. git에는 플레이스홀더(`your-domain.com`)로 커밋되어 있으므로, **서버에 복사한 뒤 반드시 실제 도메인으로 수정**하세요.

```bash
sudo vi /etc/systemd/system/jamong-mcp.service
```

```ini
# 아래 줄을 실제 도메인으로 변경
Environment=MCP_HOST=your-domain.com  →  Environment=MCP_HOST=mcp.example.com
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now jamong-mcp
```

### Claude Code 연결

CLI로 추가하거나 설정 파일에 직접 입력합니다.

**CLI (권장)**

```bash
claude mcp add jamong-skills --transport http https://your-domain.com/mcp
```

**또는 `~/.claude/settings.json` 직접 수정**

```json
{
  "mcpServers": {
    "jamong-skills": {
      "type": "http",
      "url": "https://your-domain.com/mcp"
    }
  }
}
```

연결 확인:

```bash
claude mcp list
# jamong-skills: https://your-domain.com/mcp 가 표시되면 정상
```

### Codex 연결

`~/.codex/config.yaml` 에 MCP 서버를 등록합니다.

```yaml
mcp_servers:
  - name: jamong-skills
    url: https://your-domain.com/mcp
    transport: http
```

파일이 없으면 신규 생성합니다. Codex 재시작 후 적용됩니다.

### 스킬 업데이트

```bash
cd /opt/jamong-harvest && git pull
sudo systemctl restart jamong-mcp
```

## 인코딩 기준

모든 스킬 파일은 **UTF-8 / BOM 없음 / LF** 기준으로 저장합니다. `.editorconfig`가 이 기준을 자동 적용합니다.

Windows에서 수정 시 VS Code 하단 인코딩이 `UTF-8`인지 확인하세요. `UTF-8 with BOM`이면 한글 깨짐이 발생합니다.

## 상세 가이드

스킬 설치 이후 전역 환경 적용, safety hook 설정, 새 프로젝트 템플릿 적용 절차는 아래 문서를 참고하세요.

→ [docs/guide.md](docs/guide.md)
