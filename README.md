# Jamong-Harvest

**AI로 키우는 개발농장** — Jamong의 AI 개발 환경에서 반복적으로 쓰이는 운영 규칙, 템플릿, safety hook, 적용 가이드를 모아두는 저장소입니다.

Jamong-Harvest는 Claude Code, Codex/OMX, Hermes Agent 같은 AI 코딩 에이전트가 프로젝트를 안전하고 일관되게 다룰 수 있도록 “수확 가능한 개발 과수원” 역할을 합니다.

## 목표

- Jamong 전용 AI 개발 운영 규칙을 템플릿화합니다.
- 새 프로젝트에 `CLAUDE.md` / `AGENTS.md`를 빠르게 심을 수 있게 합니다.
- `sudo` 같은 관리자 권한 명령을 차단하는 safety hook 예제를 제공합니다.
- RTK, Claude Code, Codex/OMX를 함께 사용할 때의 운영 원칙을 문서화합니다.
- 글로벌 개발 환경에 적용하는 절차를 `docs/guide.md`로 관리합니다.

## 저장소 구조

```text
Jamong-Harvest/
├── README.md
├── CLAUDE.md
├── AGENTS.md
├── templates/
│   ├── CLAUDE.md
│   └── AGENTS.md
├── hooks/
│   ├── claude/
│   │   └── block-sudo-bash.mjs
│   └── codex/
│       └── block-sudo-bash.mjs
└── docs/
    └── guide.md
```

## 빠른 사용법

새 프로젝트에 템플릿을 적용하려면:

```bash
cp /home/dev/project/Jamong-Harvest/templates/CLAUDE.md /home/dev/project/<project>/CLAUDE.md
cp /home/dev/project/Jamong-Harvest/templates/AGENTS.md /home/dev/project/<project>/AGENTS.md
```

그 다음 대상 프로젝트 파일에서 아래 placeholder를 교체합니다.

- `<PROJECT_NAME>`
- `<PROJECT_ROOT>`

글로벌 개발 환경에 적용하는 자세한 절차는 [`docs/guide.md`](docs/guide.md)를 참고하세요.

## 핵심 원칙

- 한국어 기본 응답
- `/home/dev/project/<project>` 기준 작업
- 관리자 권한 명령 직접 실행 금지
- 명시 요청 없는 commit/tag/push/deploy/restart 금지
- 작은 변경, 명확한 검증, 사용량은 추측하지 않기

## 상태

초기 템플릿 정리 단계입니다. 실제 전역 환경에 적용하기 전에는 `docs/guide.md`의 검증 절차를 먼저 수행하세요.
