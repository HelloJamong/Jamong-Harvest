---
name: admin-safety
description: >
  관리자 권한 명령 실행 금지 규칙.
  sudo, doas, pkexec 등 관리자 수준 명령을 실행하려 할 때 반드시 이 규칙을 따른다.
allowed_tools: []
run_as: inline
---

# Admin Safety Rules

## 금지 명령

다음 명령을 직접 실행해서는 안 된다:

- `sudo`
- `doas`
- `pkexec`
- `su` / `su -`
- `runuser`
- 기타 관리자 수준 패키지/시스템/서비스 명령

## 차단 시 처리 절차

관리자 권한이 필요한 경우:

1. 즉시 작업을 중지한다.
2. 아래 문구를 **정확히** 출력한다.

```text
관리자 권한이 필요한 작업이라 중지했습니다, 아래 명령어를 실행 후 이어서 진행해주세요
```

3. 사용자가 직접 실행할 정확한 명령을 제공한다.
4. 사용자가 실행 완료를 확인한 뒤에만 작업을 재개한다.

## 예시

```text
관리자 권한이 필요한 작업이라 중지했습니다, 아래 명령어를 실행 후 이어서 진행해주세요

sudo apt install build-essential
```
