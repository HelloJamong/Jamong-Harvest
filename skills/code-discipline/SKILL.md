---
name: code-discipline
description: >
  Karpathy 스타일 코딩 규율.
  코드 작성 시 항상 이 네 가지 원칙을 따른다:
  Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution.
allowed_tools: []
run_as: inline
---

# Code Discipline Rules

## Think Before Coding

- 요구사항과 성공 기준을 먼저 정리한다.
- 중요한 가정은 명시한다.
- 자료가 부족하면 파일/문서/명령으로 확인한다.
- 여러 해석이 가능하면 선택지를 제시한다. 침묵으로 선택하지 않는다.

## Simplicity First

- 요청된 문제를 해결하는 가장 작은 코드를 작성한다.
- 투기적 기능, future-proof 추상화, 불필요한 구성 가능성을 금지한다.
- 단일 사용 코드에 추상화를 도입하지 않는다.
- 불필요한 에러 핸들링, 폴백, 검증을 추가하지 않는다.

## Surgical Changes

- 작업과 직접 관련된 파일과 라인만 수정한다.
- 포맷터로 인한 대량 변경을 피한다.
- 기존 코드 스타일과 네이밍을 존중한다.
- 자신의 변경으로 생긴 미사용 코드만 제거한다. 사전에 존재하던 코드는 건드리지 않는다.
- 관련 없는 리팩터링, 주석 정리, 스타일 변경을 하지 않는다.

## Goal-Driven Execution

- 변경 후 성공 기준을 검증한다 (테스트, 린트, 타입체크, 수동 확인).
- 실패한 검증은 숨기지 않고 원인과 다음 조치를 보고한다.
- 여러 단계 작업은 각 단계마다 검증 방법을 먼저 정의한다.
