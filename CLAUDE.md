# Jamong-Harvest Agent Context

Jamong-Harvest는 Jamong의 글로벌 AI 개발 환경을 수확 가능한 템플릿과 hook 예제로 정리하는 저장소입니다.

## 이 저장소의 목적

- `templates/CLAUDE.md`: Claude Code 프로젝트 운영 템플릿
- `templates/AGENTS.md`: Codex/OMX 및 범용 에이전트 운영 템플릿
- `hooks/`: 관리자 권한 명령 차단 등 safety hook 예제
- `docs/guide.md`: 글로벌 개발 환경 적용 가이드

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
