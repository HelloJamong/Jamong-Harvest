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
│   └── versioning/
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

## 인코딩 기준

모든 스킬 파일은 **UTF-8 / BOM 없음 / LF** 기준으로 저장합니다. `.editorconfig`가 이 기준을 자동 적용합니다.

Windows에서 수정 시 VS Code 하단 인코딩이 `UTF-8`인지 확인하세요. `UTF-8 with BOM`이면 한글 깨짐이 발생합니다.

## 상세 가이드

스킬 설치 이후 전역 환경 적용, safety hook 설정, 새 프로젝트 템플릿 적용 절차는 아래 문서를 참고하세요.

→ [docs/guide.md](docs/guide.md)
