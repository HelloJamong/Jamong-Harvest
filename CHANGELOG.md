# Changelog

All notable changes to Jamong-Harvest will be documented in this file.

이 프로젝트는 Jamong의 AI 개발 운영 템플릿, safety hook, 글로벌 적용 가이드를 관리합니다.

## [Unreleased]

### Added

- Jamong-Harvest 저장소 소개를 `README.md`에 확장했습니다.
  - “AI로 키우는 개발농장” 컨셉 설명
  - 저장소 구조 문서화
  - 빠른 템플릿 적용법 추가
  - 핵심 운영 원칙 정리
- Jamong-Harvest 저장소 자체를 위한 루트 `CLAUDE.md`를 추가했습니다.
  - 저장소 목적과 작업 규칙 정의
  - 템플릿 수정 원칙 정리
- Jamong-Harvest 저장소 자체를 위한 루트 `AGENTS.md`를 추가했습니다.
  - Codex/OMX 및 범용 에이전트 운영 규칙 정의
  - 관리자 권한 금지, git/remote safety, 검증/완료 보고 규칙 포함
- 재사용 가능한 프로젝트 템플릿을 추가했습니다.
  - `templates/CLAUDE.md`: Claude Code 프로젝트 운영 템플릿
  - `templates/AGENTS.md`: Codex/OMX 및 범용 에이전트 운영 템플릿
- 관리자 권한 명령 차단 safety hook 예제를 추가했습니다.
  - `hooks/claude/block-sudo-bash.mjs`
  - `hooks/codex/block-sudo-bash.mjs`
  - `sudo`, `doas`, `pkexec` 명령 차단
  - Jamong 필수 안내 문구 출력
- 글로벌 개발 환경 적용 가이드를 추가했습니다.
  - `docs/guide.md`
  - 새 프로젝트에 템플릿 적용 절차
  - Claude Code 글로벌 메모리 적용 절차
  - Codex/OMX 글로벌 AGENTS 적용 절차
  - Claude/Codex safety hook 적용 및 검증 절차
  - RTK hook 순서와 주의사항
- git diff 리뷰용 요약 문서를 추가했습니다.
  - `docs/diff-review-summary.md`

### Verified

- `hooks/claude/block-sudo-bash.mjs` 문법 검사 통과
- `hooks/codex/block-sudo-bash.mjs` 문법 검사 통과
- `sudo apt update` payload 차단 시뮬레이션 성공
- `git status` safe command 통과 시뮬레이션 성공
- 템플릿/문서 파일 생성 및 내용 존재 확인

### Notes

- 실제 글로벌 설정 파일은 아직 수정하지 않았습니다.
- commit, tag, push, release, deploy는 수행하지 않았습니다.
- `docs/guide.md`의 `/path/to/oh-my-codex/...` 예시는 실제 환경 적용 시 설치 경로로 교체해야 합니다.
