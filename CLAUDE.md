# Jamong-Harvest Agent Context

Jamong-Harvest는 Jamong의 글로벌 AI 개발 환경을 수확 가능한 템플릿과 hook 예제로 정리하는 저장소입니다.

## 이 저장소의 목적

- `skills/`: 모든 AI에 공통 적용되는 스킬 모음 (`install.sh` / `install.bat`으로 각 LLM 경로에 설치)
- `templates/CLAUDE.md`: Claude Code 프로젝트 운영 템플릿
- `templates/AGENTS.md`: Codex/OMX 및 범용 에이전트 운영 템플릿
- `hooks/`: 관리자 권한 명령 차단 등 safety hook 예제
- `docs/guide.md`: 글로벌 개발 환경 적용 가이드

## 스킬 설치

```bash
# Claude Code에 전체 스킬 설치
./install.sh claude

# Codex에 전체 스킬 설치
./install.sh codex

# 둘 다 설치
./install.sh all

# 특정 스킬만 설치 (예: git-workflow)
./install.sh claude git-workflow

# Windows
install.bat all
```

## 제공 스킬

| 스킬 | 설명 |
|------|------|
| `git-workflow` | 브랜치/커밋/PR 규칙 |
| `admin-safety` | sudo/doas/pkexec 차단 규칙 |
| `completion-report` | 작업 완료 보고 형식 |
| `code-discipline` | Karpathy 스타일 코딩 규율 |
| `versioning` | CHANGELOG.md 기반 버전 관리 및 릴리즈 규칙 |

## 설치 경로

| LLM | 경로 |
|-----|------|
| Claude Code | `~/.claude/skills/<skill>/SKILL.md` |
| Codex | `~/.agents/skills/<skill>/SKILL.md` |
| Codex (호환) | `~/.codex/skills/<skill>/SKILL.md` |

## 작업 규칙

- 기본 응답은 한국어로 합니다.
- 이 저장소의 루트는 `/home/dev/project/Jamong-Harvest` 입니다.
- 명시 요청 없이 commit/tag/push/deploy/restart를 수행하지 않습니다.
- `sudo`, `doas`, `pkexec` 등 관리자 권한 명령을 직접 실행하지 않습니다.
- 변경 후 가능한 범위에서 `git diff`, 문서 구조 확인, 스크립트 문법 검사를 수행합니다.

## 템플릿 수정 원칙

- 템플릿은 다른 프로젝트에 복사해도 이해되도록 자체 설명을 포함합니다.
- 프로젝트 고유 값은 `<PROJECT_NAME>`, `<PROJECT_ROOT>` 같은 placeholder로 둡니다.
- Jamong 전용 불변 규칙은 명확히 유지합니다.
- hook 예제는 실제 전역 설정에 적용하기 전 검증 명령을 함께 문서화합니다.
