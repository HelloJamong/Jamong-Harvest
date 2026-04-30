# Git Diff Review Summary

Date: 2026-04-30

## 요약

이번 변경은 Jamong-Harvest 저장소를 “Jamong 전용 AI 개발 운영 템플릿 저장소”로 정리하는 초기 구조화 작업입니다. 기존의 짧은 README에서 확장하여, 프로젝트 소개/템플릿/safety hook/글로벌 적용 가이드까지 포함하는 문서 중심의 변경입니다.

## 변경 파일별 리뷰 요약

### `README.md`

- Jamong-Harvest 소개를 확장했습니다.
- “AI로 키우는 개발농장” 컨셉을 설명했습니다.
- 저장소 구조, 빠른 사용법, 핵심 원칙, 글로벌 적용 가이드 링크를 추가했습니다.

리뷰 포인트:
- 저장소 목적이 명확합니다.
- 실제 사용자가 먼저 볼 진입점으로 적합합니다.
- 빠른 사용법은 `templates/CLAUDE.md`, `templates/AGENTS.md` 복사 흐름을 잘 안내합니다.

### `CLAUDE.md`

- 저장소 루트의 `CLAUDE.md`는 Jamong-Harvest 자체를 위한 agent context로 정리했습니다.
- 템플릿 본문은 `templates/CLAUDE.md`로 분리했습니다.

리뷰 포인트:
- 루트 context와 재사용 템플릿의 역할 분리가 적절합니다.
- 저장소 작업 규칙이 짧고 명확합니다.

### `AGENTS.md`

- Jamong-Harvest 저장소 자체에서 Codex/OMX 및 범용 에이전트가 따를 운영 규칙을 추가했습니다.
- 관리자 권한 금지, git/remote safety, 검증/완료 보고 규칙을 포함했습니다.

리뷰 포인트:
- Claude 외 에이전트도 동일한 안전 경계를 따르도록 보완되었습니다.
- Codex/OMX 실행 관례(`omx --madmax --high`)가 반영되었습니다.

### `templates/CLAUDE.md`

- 다른 프로젝트에 복사 가능한 Claude Code 운영 템플릿을 추가했습니다.
- `<PROJECT_NAME>`, `<PROJECT_ROOT>` placeholder를 사용해 재사용 가능하게 구성했습니다.
- Jamong의 핵심 개발 운영 규칙을 포함했습니다.

리뷰 포인트:
- 프로젝트별 적용 시 수정해야 할 위치가 명확합니다.
- 관리자 권한 금지 문구가 정확히 포함되어 있습니다.
- commit/tag/push/deploy/restart 금지 규칙이 명확합니다.

### `templates/AGENTS.md`

- 다른 프로젝트에 복사 가능한 Codex/OMX 및 범용 에이전트 운영 템플릿을 추가했습니다.
- Claude 전용이 아닌 범용 agent context에 맞게 영어 섹션명과 한국어 운영 규칙을 혼합했습니다.

리뷰 포인트:
- 범용 agent가 이해하기 쉬운 구조입니다.
- Jamong 환경의 안전 규칙과 검증 루틴이 충분히 포함되어 있습니다.

### `hooks/claude/block-sudo-bash.mjs`

- Claude Code Bash `PreToolUse`에서 `sudo`, `doas`, `pkexec` 명령을 차단하는 예제 hook을 추가했습니다.
- 차단 시 Jamong의 필수 안내 문구와 정확한 명령을 반환합니다.

리뷰 포인트:
- `node --check` 문법 검사를 통과했습니다.
- payload 시뮬레이션에서 `sudo apt update` 차단을 확인했습니다.
- safe command인 `git status`는 출력 없이 통과합니다.

### `hooks/codex/block-sudo-bash.mjs`

- Codex/OMX native hook용 동일 safety hook 예제를 추가했습니다.

리뷰 포인트:
- Claude hook과 동일한 동작을 합니다.
- Codex/OMX native hook 설정에 연결하기 쉽습니다.

### `docs/guide.md`

- Jamong-Harvest를 글로벌 개발 환경에 적용하는 절차를 작성했습니다.
- 새 프로젝트 템플릿 적용, Claude 글로벌 메모리, Codex/OMX 글로벌 AGENTS, safety hook 적용, RTK 순서, 검증 체크리스트를 포함했습니다.

리뷰 포인트:
- 직접 복붙 가능한 명령과 설정 예시가 포함되어 있습니다.
- 기존 OMC/OMX/RTK 설정을 덮어쓰지 말고 병합하라는 주의가 포함되어 있습니다.
- 전역 설정 적용 전 검증 단계가 명확합니다.

### `CHANGELOG.md`

- 이번 초기 구조화 작업의 초안 changelog를 추가했습니다.

## 품질/안전 검토

### 확인된 사항

- 관리자 권한 명령을 직접 실행하지 않았습니다.
- commit/tag/push/deploy/restart를 수행하지 않았습니다.
- hook 스크립트 문법 검사를 통과했습니다.
- hook payload 시뮬레이션을 통해 차단/통과 동작을 확인했습니다.
- 문서와 템플릿은 시크릿/토큰을 포함하지 않습니다.

### 주의할 점

- `docs/guide.md`의 Codex/OMX native hook 경로 `/path/to/oh-my-codex/...`는 실제 환경 적용 시 교체해야 합니다.
- 전역 설정 파일(`/home/dev/.claude/CLAUDE.md`, `/home/dev/.codex/AGENTS.md`, settings/hooks 파일)은 아직 실제로 수정하지 않았습니다.
- 현재 변경 파일들은 아직 커밋되지 않았습니다.

## 권장 커밋 메시지

```text
feat: add Jamong AI development templates and safety hooks
```

또는 한국어 커밋을 선호하면:

```text
feat: Jamong AI 개발 환경 템플릿과 safety hook 추가
```
