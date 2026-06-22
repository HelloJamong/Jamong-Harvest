---
name: git-workflow
description: >
  Git 작업 전 반드시 확인해야 할 브랜치/커밋 규칙.
  다음 상황에서 반드시 이 스킬을 먼저 확인한다:
  (1) git add / commit / push / branch / merge / rebase 등 git 명령어를 실행할 때
  (2) 브랜치를 생성하거나 전환할 때
  (3) 변경사항을 커밋할 때
allowed_tools: []
run_as: inline
---

# Git Workflow Rules

## 기본 규칙

- **커밋 내용은 한국어**로 작성한다.
- **커밋 제목은 명사형 종결.** 문장형으로 끝내지 않는다.
  - ✅ `feat: README.md 파일 수정`
  - ❌ `feat: README.md 파일을 수정했습니다.`
- **커밋 제목 접두사:** `feat:`, `fix:`, `chore:`, `docs:` 중 하나만 사용
- **`main`에 직접 커밋·푸시 허용** — 브랜치 작업은 선택 사항이다.
- **브랜치 이름 형식 (브랜치를 사용할 경우):** `feat/`, `fix/`, `chore/`, `docs/` 접두사 사용
  - 예: `feat/oauth-login`, `fix/npe-error`, `chore/deps-update`
- **명시 요청 없이 commit / tag / push / deploy 절대 금지**
  - 작업이 완료되어도 커밋하지 않는다.
  - 사용자가 "커밋해줘", "푸시해줘", "배포해줘" 등 명시적으로 요청할 때만 실행한다.
  - 한 번 승인을 받았다고 이후 작업에서도 자동으로 실행하지 않는다. 매번 별도 요청이 필요하다.

## 관련 스킬

- **versioning**: 버전 태그 생성·CHANGELOG 작성이 포함된 커밋 시 함께 확인한다.
- **completion-report**: 작업 커밋 완료 후 보고 형식을 작성할 때 함께 확인한다.
