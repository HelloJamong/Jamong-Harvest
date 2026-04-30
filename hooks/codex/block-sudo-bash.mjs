#!/usr/bin/env node

/**
 * Jamong safety hook example for Claude Code / Codex native Bash PreToolUse hooks.
 *
 * Purpose:
 * - Deny administrator-level shell commands before an AI coding agent runs them.
 * - Print Jamong's required Korean stop message and the exact blocked command.
 *
 * Install examples:
 * - Claude Code: copy to /home/dev/.claude/hooks/block-sudo-bash.mjs
 * - Codex/OMX: copy to /home/dev/.codex/hooks/block-sudo-bash.mjs
 */

const REQUIRED_MESSAGE = '관리자 권한이 필요한 작업이라 중지했습니다, 아래 명령어를 실행 후 이어서 진행해주세요'

function readStdin() {
  return new Promise((resolve, reject) => {
    let data = ''
    process.stdin.setEncoding('utf8')
    process.stdin.on('data', chunk => { data += chunk })
    process.stdin.on('end', () => resolve(data))
    process.stdin.on('error', reject)
  })
}

function getCommand(payload) {
  const input = payload?.tool_input ?? payload?.toolInput ?? payload?.input ?? {}
  if (typeof input?.command === 'string') return input.command
  if (typeof payload?.command === 'string') return payload.command
  return ''
}

function isBashTool(payload) {
  const toolName = payload?.tool_name ?? payload?.toolName ?? payload?.tool
  return toolName === 'Bash' || toolName === 'BashTool'
}

function isAdminCommand(command) {
  return /^\s*(sudo|doas|pkexec)\b/.test(command)
}

try {
  const raw = await readStdin()
  if (!raw.trim()) process.exit(0)

  const payload = JSON.parse(raw)
  const command = getCommand(payload)

  if (isBashTool(payload) && isAdminCommand(command)) {
    const reason = `${REQUIRED_MESSAGE}

${command}`
    process.stdout.write(JSON.stringify({
      permissionDecision: 'deny',
      permissionDecisionReason: reason,
    }))
  }
} catch (error) {
  // Fail open so malformed hook payloads do not brick unrelated agent usage.
  process.stderr.write(`[block-sudo-bash] ${error instanceof Error ? error.message : String(error)}
`)
  process.exit(0)
}
