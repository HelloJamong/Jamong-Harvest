---
name: versioning
description: >
  버전 관리 및 릴리즈 규칙.
  다음 상황에서 반드시 이 스킬을 먼저 확인한다:
  (1) 버전을 올리거나 릴리즈를 준비할 때
  (2) CHANGELOG.md를 작성하거나 수정할 때
  (3) git tag를 생성하거나 push할 때
  (4) GitHub Release를 생성할 때
allowed_tools: []
run_as: inline
---

# Versioning Rules

## 버전 형식

```
YY.메이저.마이너
```

- `YY`: 연도 두 자리 (예: 25, 26)
- `메이저`: 기능 추가 또는 하위 호환 불가 변경 시 증가
- `마이너`: 버그 수정 또는 하위 호환 변경 시 증가

예시: `25.1.0`, `25.2.3`, `26.1.0`

## CHANGELOG.md 규칙

- **버전 관리는 반드시 CHANGELOG.md로 한다.**
- 새 버전마다 아래 형식으로 항목을 추가한다.

```markdown
## [YY.메이저.마이너] - YYYY-MM-DD

### Added
- 새로 추가된 기능

### Changed
- 변경된 동작

### Fixed
- 수정된 버그

### Removed
- 제거된 항목
```

- 변경이 없는 섹션(Added/Changed/Fixed/Removed)은 생략한다.
- 최신 버전이 항상 파일 상단에 위치한다.

## Tag 및 Release 규칙

- **명시 요청 없이 tag 생성/push 금지.**
- tag 이름은 버전과 동일하게 한다: `25.1.0`
- GitHub Release 생성 시 **해당 버전의 CHANGELOG.md 내용을 그대로 본문에 반영**한다.

### 릴리즈 절차

1. CHANGELOG.md에 해당 버전 항목 작성
2. 변경 사항 커밋: `chore: 25.1.0 릴리즈`
3. 태그 생성: `git tag 25.1.0`
4. 태그 push: `git push origin 25.1.0`
5. GitHub Release 생성 — 본문: 해당 버전 CHANGELOG.md 내용
