# Changelog

All notable changes to Jamong-Harvest will be documented in this file.

이 프로젝트는 Jamong의 AI 개발 운영 템플릿, 공통 스킬, safety hook, 글로벌 적용 가이드를 관리합니다.

버전 형식: `YY.메이저.마이너`

---

## [26.1.2] - 2026-06-05

### Changed

- `README.md`: 스킬 설치(`install.sh` / `install.bat`) 위주로 재작성, 상세 가이드 내용은 `docs/guide.md` 링크로 대체
- `docs/guide.md`: 스킬 설치 섹션 신설 및 구버전 내용 현행화
  - 구성요소 테이블에 `skills/`, `install.sh`, `install.bat` 추가
  - Linux/macOS/Windows 스킬 설치 절차 추가
  - 전역 설정, hook 적용, RTK 주의사항, 점검 체크리스트 정리

---

## [26.1.1] - 2026-06-05

### Added

- 공통 스킬 구조 신설 (`skills/`)
  - `skills/git-workflow/SKILL.md`: 브랜치/커밋/PR 규칙
  - `skills/admin-safety/SKILL.md`: sudo/doas/pkexec 차단 규칙
  - `skills/completion-report/SKILL.md`: 작업 완료 보고 형식
  - `skills/code-discipline/SKILL.md`: Karpathy 스타일 코딩 규율
  - `skills/versioning/SKILL.md`: CHANGELOG.md 기반 버전 관리 및 릴리즈 규칙
- 스킬 설치 스크립트 추가
  - `install.sh`: Linux/macOS — Claude Code / Codex 경로 자동 설치 (`skills/` 동적 스캔)
  - `install.bat`: Windows — 동일 기능
- `.editorconfig` 추가: UTF-8 / LF / BOM 없음 강제 적용 (한글 깨짐 방지)
- `README.md` 업데이트: 저장소 구조, 스킬 설치 가이드, 인코딩 주의사항 추가
- `CLAUDE.md` 업데이트: 스킬 목록 및 설치 경로 섹션 추가
- 초기 프로젝트 구성
  - `templates/CLAUDE.md`: Claude Code 프로젝트 운영 템플릿
  - `templates/AGENTS.md`: Codex/OMX 및 범용 에이전트 운영 템플릿
  - `hooks/claude/block-sudo-bash.mjs`: Claude Code sudo 차단 hook
  - `hooks/codex/block-sudo-bash.mjs`: Codex sudo 차단 hook
  - `docs/guide.md`: 글로벌 개발 환경 적용 가이드

### Fixed

- Codex 스킬 경로 이중 등록 (`~/.agents/skills/`, `~/.codex/skills/`) — Codex 버전별 경로 차이 대응

### Notes

- 스킬 파일은 Claude Code / Codex 공통 YAML frontmatter 형식 사용. 파일 분리 없이 단일 소스로 양쪽 설치.
- 새 스킬 추가 시 `skills/<name>/SKILL.md`만 작성하면 `install.sh`가 자동 인식.
- commit, tag, push, release, deploy는 수행하지 않았습니다.
