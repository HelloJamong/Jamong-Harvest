---
name: git-workflow
description: >
  Git 작업 전 반드시 확인해야 할 브랜치/커밋/PR 규칙.
  다음 상황에서 반드시 이 스킬을 먼저 확인한다:
  (1) git add / commit / push / branch / merge / rebase 등 git 명령어를 실행할 때
  (2) Pull Request를 생성하거나 리뷰할 때
  (3) 브랜치를 생성하거나 전환할 때
  (4) 변경사항을 커밋할 때
allowed_tools: []
run_as: inline
---

# Git Workflow Rules

## 기본 규칙

- **커밋/PR 내용은 한국어**로 작성한다.
- **커밋 제목과 PR 제목은 명사형 종결.** 문장형으로 끝내지 않는다.
  - ✅ `feat: README.md 파일 수정`
  - ❌ `feat: README.md 파일을 수정했습니다.`
- **브랜치 이름 형식:** `feat/`, `fix/`, `chore/`, `docs/` 접두사 필수
  - 예: `feat/oauth-login`, `fix/npe-error`, `chore/deps-update`
- **보호 브랜치 직접 커밋/푸시 금지:** `main`, `master`, `develop`
  - 반드시 PR을 통해서만 병합한다.
- **커밋 제목 접두사:** `feat:`, `fix:`, `chore:`, `docs:` 중 하나만 사용
- **PR은 반드시 squash merge**
- **명시 요청 없이 commit / tag / push / deploy 금지**

## PR 생성 규칙

- **PR base branch를 추측하지 말 것.** 사용자에게 직접 확인한다.
- 저장소에 `develop` 브랜치가 있으면 feature 계열의 기본 base는 `develop`
- `hotfix/*` 브랜치만 `main`/`master` 대상 PR 후보
- **PR 본문 형식:**
  ```markdown
  ## 요약
  ## 테스트
  ## 리스크
  ```

## PR 생성 전 필수 확인

1. `git branch --show-current` — 현재 브랜치 확인
2. 저장소 로컬의 `AGENTS.md` / `CLAUDE.md` 확인
3. 배포가 `main` push에 묶여 있는지 확인
4. 보호 브랜치 규칙 위반 여부 확인
