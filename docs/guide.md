# Jamong-Harvest 글로벌 개발 환경 적용 가이드

이 문서는 Jamong-Harvest의 템플릿과 safety hook을 Jamong의 글로벌 AI 개발 환경에 적용하는 방법을 설명합니다.

> 원칙: 전역 설정은 영향 범위가 크므로 먼저 백업하고, 문법 검증과 payload 시뮬레이션을 통과한 뒤 적용합니다.

## 1. 구성 요소

| 경로 | 용도 |
| --- | --- |
| `templates/CLAUDE.md` | Claude Code 프로젝트별 운영 규칙 템플릿 |
| `templates/AGENTS.md` | Codex/OMX 및 범용 에이전트 운영 규칙 템플릿 |
| `hooks/claude/block-sudo-bash.mjs` | Claude Code Bash PreToolUse 관리자 명령 차단 예제 |
| `hooks/codex/block-sudo-bash.mjs` | Codex/OMX Bash PreToolUse 관리자 명령 차단 예제 |
| `docs/guide.md` | 글로벌 적용 절차 |

## 2. 새 프로젝트에 템플릿 적용

대상 프로젝트가 `/home/dev/project/<project>`에 있다고 가정합니다.

```bash
PROJECT=/home/dev/project/<project>
cp /home/dev/project/Jamong-Harvest/templates/CLAUDE.md "$PROJECT/CLAUDE.md"
cp /home/dev/project/Jamong-Harvest/templates/AGENTS.md "$PROJECT/AGENTS.md"
```

그 다음 대상 파일에서 placeholder를 교체합니다.

```text
<PROJECT_NAME>
<PROJECT_ROOT>
```

권장 확인:

```bash
cd "$PROJECT"
git status --short --branch
git diff -- CLAUDE.md AGENTS.md
```

## 3. Claude Code 글로벌 메모리에 Jamong 규칙 반영

Claude Code 글로벌 메모리 파일:

```text
/home/dev/.claude/CLAUDE.md
```

적용 원칙:

1. 기존 파일을 먼저 백업합니다.
2. OMC 같은 도구가 관리하는 블록이 있다면 내부를 수정하지 않습니다.
3. Jamong 전용 규칙은 관리 블록 바깥에 별도 섹션으로 추가합니다.

예시 섹션 제목:

```md
# Jamong Global Project Working Guidelines
```

포함할 핵심 규칙:

- 한국어 기본 응답
- 프로젝트 루트는 `/home/dev/project/<project>`
- `sudo`/관리자 명령 직접 실행 금지
- 명시 요청 없는 commit/tag/push/deploy/restart 금지
- 변경 후 diff/test/lint/security 검증
- Claude Code 사용량 70% 근처 경고, 90% 이상이면 Codex/OMX 고려
- Codex는 Jamong 환경에서 보통 `omx --madmax --high`로 실행

## 4. Codex/OMX 글로벌 AGENTS에 Jamong 규칙 반영

Codex/OMX 글로벌 지침 파일:

```text
/home/dev/.codex/AGENTS.md
```

적용 원칙은 Claude와 동일합니다.

- 기존 OMX/도구 생성 블록을 보존합니다.
- Jamong 전용 운영 규칙을 별도 섹션으로 추가합니다.
- RTK 안내 파일을 사용하는 경우 기존 `@/home/dev/.codex/RTK.md` 참조를 보존합니다.

## 5. Claude Code safety hook 적용

### 5.1 hook 파일 복사

```bash
mkdir -p /home/dev/.claude/hooks
cp /home/dev/project/Jamong-Harvest/hooks/claude/block-sudo-bash.mjs /home/dev/.claude/hooks/block-sudo-bash.mjs
chmod +x /home/dev/.claude/hooks/block-sudo-bash.mjs
```

### 5.2 settings.json 예시

대상 파일:

```text
/home/dev/.claude/settings.json
```

권장 hook 순서:

1. Jamong 관리자 권한 차단 hook
2. RTK rewrite hook

예시:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "node /home/dev/.claude/hooks/block-sudo-bash.mjs",
            "timeout": 5
          },
          {
            "type": "command",
            "command": "rtk hook claude",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

이미 다른 hook이 있다면 덮어쓰지 말고 병합합니다.

### 5.3 Claude hook 검증

```bash
python3 -m json.tool /home/dev/.claude/settings.json >/dev/null
node --check /home/dev/.claude/hooks/block-sudo-bash.mjs
```

payload 시뮬레이션:

```bash
printf '%s
' '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"sudo apt update"}}'   | node /home/dev/.claude/hooks/block-sudo-bash.mjs
```

예상 결과:

- JSON에 `"permissionDecision":"deny"` 포함
- 아래 문구 포함

```text
관리자 권한이 필요한 작업이라 중지했습니다, 아래 명령어를 실행 후 이어서 진행해주세요
```

safe command는 아무 출력 없이 통과해야 합니다.

```bash
printf '%s
' '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"git status"}}'   | node /home/dev/.claude/hooks/block-sudo-bash.mjs
```

## 6. Codex/OMX safety hook 적용

### 6.1 hook 파일 복사

```bash
mkdir -p /home/dev/.codex/hooks
cp /home/dev/project/Jamong-Harvest/hooks/codex/block-sudo-bash.mjs /home/dev/.codex/hooks/block-sudo-bash.mjs
chmod +x /home/dev/.codex/hooks/block-sudo-bash.mjs
```

### 6.2 Codex native hooks 활성화 확인

대상 파일:

```text
/home/dev/.codex/config.toml
```

필요 설정:

```toml
[features]
codex_hooks = true
```

확인 예시:

```bash
codex features list | grep codex_hooks
omx doctor
```

### 6.3 hooks.json 예시

대상 파일:

```text
/home/dev/.codex/hooks.json
```

권장 hook 순서:

1. OMX native policy hook
2. Jamong 관리자 권한 차단 hook
3. RTK rewrite hook

예시:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "node /path/to/oh-my-codex/dist/scripts/codex-native-hook.js",
            "timeout": 5
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "node /home/dev/.codex/hooks/block-sudo-bash.mjs",
            "timeout": 5
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "rtk hook claude",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

`/path/to/oh-my-codex/...`는 실제 설치 경로로 교체합니다. 기존 `hooks.json`이 있으면 덮어쓰지 말고 병합합니다.

### 6.4 Codex hook 검증

```bash
python3 -m json.tool /home/dev/.codex/hooks.json >/dev/null
node --check /home/dev/.codex/hooks/block-sudo-bash.mjs
```

payload 시뮬레이션:

```bash
printf '%s
' '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"sudo apt update"},"cwd":"/home/dev/project"}'   | node /home/dev/.codex/hooks/block-sudo-bash.mjs
```

safe command + RTK 확인:

```bash
printf '%s
' '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"git status"},"cwd":"/home/dev/project/<project>"}'   | rtk hook claude
```

예상: `updatedInput.command`가 `rtk git status` 형태로 변환됩니다.

## 7. RTK 적용 시 주의사항

- `rtk hook codex`가 없을 수 있습니다. 확인 없이 문서나 설정에 넣지 않습니다.
- 현재 알려진 방식은 Codex native hook payload에 `rtk hook claude`를 사용하는 것입니다.
- 관리자 권한 차단 hook은 항상 RTK rewrite보다 먼저 둡니다.
- Claude/Codex의 내장 파일 읽기/검색 도구는 Bash hook을 거치지 않을 수 있습니다.

## 8. 적용 후 점검 체크리스트

- [ ] 새 프로젝트에 `CLAUDE.md`, `AGENTS.md`가 복사되었다.
- [ ] `<PROJECT_NAME>`, `<PROJECT_ROOT>` placeholder가 실제 값으로 교체되었다.
- [ ] `/home/dev/.claude/CLAUDE.md`에 Jamong 글로벌 규칙이 관리 블록 밖에 반영되었다.
- [ ] `/home/dev/.codex/AGENTS.md`에 Jamong 글로벌 규칙이 관리 블록 밖에 반영되었다.
- [ ] Claude hook script가 `node --check`를 통과했다.
- [ ] Codex hook script가 `node --check`를 통과했다.
- [ ] `sudo apt update` payload가 deny 된다.
- [ ] `git status` payload는 safety hook에서 통과한다.
- [ ] RTK를 사용할 경우 safe command rewrite가 정상 동작한다.
- [ ] 기존 OMC/OMX/RTK 설정을 덮어쓰지 않고 병합했다.

## 9. 운영 팁

- 전역 설정 변경 전후로 diff를 남겨둡니다.
- hook은 timeout을 짧게 둡니다. 예: `timeout: 5`.
- 사용량은 신뢰 가능한 source가 있을 때만 보고하고, 없으면 `확인불가`로 표시합니다.
- commit/tag/push/deploy는 Jamong이 명시적으로 요청했을 때만 수행합니다.
