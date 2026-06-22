# Jamong-Harvest SPEC

> 이 문서는 Jamong-Harvest의 현재 상태를 있는 그대로 기술한 레퍼런스 명세입니다.
> 신규 기여자 또는 AI 에이전트가 프로젝트를 빠르게 파악하는 용도로 사용합니다.

---

## 1. 목표 (Objective)

Jamong의 AI 개발 환경에서 반복적으로 쓰이는 **공통 스킬, 운영 템플릿, safety hook**을 단일 저장소에서 관리하고, 새 머신·새 프로젝트에 `install.sh` 한 번으로 즉시 적용할 수 있게 한다.  
추가로 **MCP 서버**를 통해 스킬 콘텐츠를 외부 AI 도구에 OAuth 2.0 인증 기반으로 제공한다.

**대상 사용자**
- Jamong (저장소 소유자) — 새 프로젝트 시작 시 또는 환경 재구성 시 사용
- AI 에이전트 (Claude Code, Codex/OMX) — 저장소 작업 시 이 파일을 운영 지침으로 참조

**현재 버전**: `26.4.4`  
**버전 형식**: `YY.메이저.마이너`

---

## 2. 명령어 (Commands)

| 명령어 | 설명 |
|--------|------|
| `./install.sh claude` | Claude Code에 전체 스킬 설치 (`~/.claude/skills/`) |
| `./install.sh codex` | Codex에 전체 스킬 설치 (`~/.agents/skills/`, `~/.codex/skills/`) |
| `./install.sh all` | Claude Code + Codex 모두 설치 |
| `./install.sh claude <skill>` | 특정 스킬만 Claude Code에 설치 |
| `install.bat all` | Windows — Claude Code + Codex 모두 설치 |
| `./mcp/install.sh` | MCP 서버 systemd 서비스 설치 및 시작 |
| `git tag <version>` | 버전 태그 생성 (push하면 GitHub Actions가 Release 자동 생성) |

**검증 명령어** (변경 후 필수 실행)

```bash
# hook 문법 검사
node --check hooks/claude/block-sudo-bash.mjs
node --check hooks/codex/block-sudo-bash.mjs

# 설치 스크립트 문법 검사
bash -n install.sh
bash -n mcp/install.sh

# sudo 차단 동작 확인
printf '%s\n' '{"tool_name":"Bash","tool_input":{"command":"sudo apt update"}}' \
  | node hooks/claude/block-sudo-bash.mjs
# 예상: permissionDecision:"deny" + 한국어 안내 출력

# safe command 통과 확인
printf '%s\n' '{"tool_name":"Bash","tool_input":{"command":"git status"}}' \
  | node hooks/claude/block-sudo-bash.mjs
# 예상: 아무 출력 없이 종료 코드 0

# MCP 서버 구문 검사
python3 -m py_compile mcp/server.py

# MCP 서버 기동 확인 (로컬, PORT=8080)
PORT=8080 python3 mcp/server.py &
sleep 1
curl -s http://localhost:8080/.well-known/oauth-authorization-server | python3 -m json.tool
kill %1
```

---

## 3. 프로젝트 구조 (Project Structure)

```text
Jamong-Harvest/
├── install.sh              # Linux/macOS 스킬 설치 스크립트 (동적 스캔)
├── install.bat             # Windows 스킬 설치 스크립트
├── skills/                 # Claude Code / Codex 공통 스킬
│   ├── git-workflow/SKILL.md       # 브랜치/커밋 규칙 (main 직접 푸시 허용)
│   ├── admin-safety/SKILL.md       # sudo/doas/pkexec 차단 규칙
│   ├── completion-report/SKILL.md  # 작업 완료 보고 형식
│   ├── code-discipline/SKILL.md    # Karpathy 스타일 코딩 규율
│   ├── versioning/SKILL.md         # CHANGELOG 기반 버전·릴리즈 규칙
│   └── deploy/SKILL.md             # Docker 이미지 배포 규칙 (digest 기반)
├── mcp/                    # MCP 서버 (FastMCP + OAuth 2.0)
│   ├── server.py               # FastMCP 서버 본체 — OAuth 인증, skills 리소스 제공
│   ├── install.sh              # systemd 서비스 설치 스크립트
│   ├── jamong-mcp.service      # systemd unit 템플릿
│   ├── jamong-mcp.env.example  # 환경변수 템플릿 (PORT, MCP_HOST, SERVER_URL, MCP_USERNAME, MCP_PASSWORD)
│   └── requirements.txt        # Python 의존성 (mcp[cli]>=1.28.0, uvicorn, pydantic)
├── templates/
│   ├── CLAUDE.md           # Claude Code 프로젝트 운영 템플릿
│   └── AGENTS.md           # Codex/OMX 및 범용 에이전트 운영 템플릿
├── hooks/
│   ├── claude/block-sudo-bash.mjs  # Claude Code Bash PreToolUse hook
│   └── codex/block-sudo-bash.mjs   # Codex Bash PreToolUse hook
├── docs/
│   └── guide.md            # 글로벌 환경 적용 가이드
├── .github/workflows/
│   └── release.yml         # 버전 태그 push → install.zip + GitHub Release 자동 생성
├── CLAUDE.md               # 이 저장소의 AI 에이전트 운영 지침
├── AGENTS.md               # Codex/OMX 운영 지침
├── CHANGELOG.md            # 버전 히스토리
└── .editorconfig           # UTF-8 / LF / BOM 없음 강제
```

**핵심 설계 결정**

- 스킬은 단일 파일(`SKILL.md`)로 관리 — Claude Code / Codex 공통 YAML frontmatter 사용, 플랫폼별 파일 분리 없음
- `install.sh`는 `skills/` 디렉터리를 동적으로 스캔 — 새 스킬 추가 시 스크립트 수정 불필요
- MCP 서버는 `mcp/server.py` 단일 파일 — 인메모리 토큰 저장, 재시작 시 세션 초기화 (의도된 설계)
- MCP 인증: OAuth 2.0 PKCE 플로우, 브라우저 로그인 페이지 (`/login`) 제공
- GitHub Actions는 `YY.N.N` 패턴 태그에만 트리거됨

---

## 4. 코드 스타일 (Code Style)

### 스킬 파일 (`SKILL.md`)

```markdown
---
name: <skill-name>
description: >
  트리거 조건 설명.
  (1) 상황1
  (2) 상황2
allowed_tools: []
run_as: inline
---

# <Title>
...본문...
```

- 인코딩: **UTF-8 / BOM 없음 / LF**
- 언어: 한국어 본문, YAML key는 영어

### 쉘 스크립트 (`install.sh`, `mcp/install.sh`)

- 첫 줄: `#!/usr/bin/env bash`
- 두 번째 줄: `set -euo pipefail`
- 함수명: snake_case
- 지역 변수: `local` 명시

### Hook (`*.mjs`)

- Node.js ESM 모듈
- stdin JSON 파싱 → `permissionDecision` 결과 stdout 출력 구조
- `sudo`, `doas`, `pkexec`, `su -`, `runuser` 탐지 시 deny

### MCP 서버 (`mcp/server.py`)

- Python 3.10+, 타입 힌트 필수
- `FastMCP` (PyPI `mcp[cli]>=1.28.0`) 사용
- 환경변수: `PORT`, `MCP_HOST`, `SERVER_URL`, `MCP_USERNAME`, `MCP_PASSWORD`
- 실제 환경변수 파일(`mcp/*.env`)은 `.gitignore` 처리 — `jamong-mcp.env.example`만 커밋

### 템플릿 (`templates/*.md`)

- 프로젝트 고유 값은 `<PROJECT_NAME>`, `<PROJECT_ROOT>` placeholder 사용
- 다른 프로젝트에 복사해도 자체 설명이 되어야 함

---

## 5. 테스트 전략 (Testing Strategy)

이 저장소는 별도의 테스트 프레임워크가 없음. 검증은 아래 수동 절차로 수행:

| 대상 | 검증 방법 |
|------|-----------|
| `install.sh` 문법 | `bash -n install.sh` |
| `mcp/install.sh` 문법 | `bash -n mcp/install.sh` |
| hook 문법 | `node --check <hook>.mjs` |
| hook sudo 차단 | `printf` + `node` pipe 테스트 (deny 확인) |
| hook safe pass | `printf` + `node` pipe 테스트 (무출력 확인) |
| 스킬 설치 결과 | `./install.sh claude` 후 `ls ~/.claude/skills/` |
| 인코딩 | `.editorconfig` 준수 여부 — `file <skill>.md` 로 확인 |
| MCP 서버 구문 | `python3 -m py_compile mcp/server.py` |
| MCP OAuth 엔드포인트 | 로컬 기동 후 `curl /.well-known/oauth-authorization-server` JSON 확인 |

**향후 과제**: GitHub Actions에 자동 검증 step 추가 고려 (hook 동작 + MCP 서버 smoke test)

---

## 6. 경계 (Boundaries)

### Always Do (항상 수행)
- 변경 후 `git diff`로 변경 범위 확인
- 스킬 파일 수정 시 UTF-8 / LF 인코딩 유지
- 새 스킬 추가 시 `CHANGELOG.md`에 Added 항목 기록
- SKILL.md YAML frontmatter 형식 준수
- `mcp/*.env` 실제 파일은 절대 커밋하지 않음 (`.gitignore` 보호)

### Ask First (먼저 확인)
- 기존 스킬 내용을 실질적으로 변경하는 경우
- 새 설치 경로(플랫폼) 추가
- GitHub Actions 워크플로우 변경
- 전역 설정 파일(`~/.claude/`, `~/.codex/`) 수정
- MCP OAuth 플로우 변경 (토큰 저장 방식, 세션 유지 방식 등)

### Never Do (절대 금지)
- 명시 요청 없이 `commit / tag / push / deploy`
- `sudo`, `doas`, `pkexec` 직접 실행
- 스킬 파일을 LLM별로 분리 (단일 소스 원칙 위반)
- 테스트 없이 hook 로직 변경
- `install.sh`를 동적 스캔에서 정적 목록 방식으로 퇴행
- `mcp/*.env` 파일을 git에 커밋

---

*최종 갱신: 2026-06-22 (v26.4.4 기준)*
