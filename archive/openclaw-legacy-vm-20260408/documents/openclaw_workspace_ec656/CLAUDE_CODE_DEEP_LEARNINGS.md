# Claude Code 源码深度学习笔记

## 源码位置

```
~/.openclaw/workspace/claude-code-sourcemap/
├── claude-code-2.1.88.tgz    # 原始包（永久备份）
├── restored-src/              # 提取的源码
│   └── src/
│       ├── coordinator/       # 协调器模式
│       ├── tools/             # 工具定义（20+ 工具）
│       ├── hooks/             # React hooks + 权限钩子
│       ├── skills/            # 技能系统
│       ├── state/             # 状态管理
│       ├── query/             # 查询引擎
│       └── constants/         # 系统提示词分区
└── package/                   # npm 包内容
```

---

## 核心设计学习

### 1. Coordinator Mode（协调器模式）

**文件**: `src/coordinator/coordinatorMode.ts`

**核心思想**:
- Coordinator 不执行工具，只分发任务
- Worker 执行实际工作
- 工具白名单隔离

**关键设计**:
```typescript
// Coordinator 可用工具
const COORDINATOR_TOOLS = [
  'Agent',        // 启动 Worker
  'SendMessage',  // 继续 Worker
  'TaskStop',     // 停止 Worker
]

// Worker 可用工具（白名单）
const ASYNC_AGENT_ALLOWED_TOOLS = new Set([
  'Bash', 'Read', 'Edit', 'Write', 'Glob', 'Grep', 'LSP', 'Skill', ...
])
```

**OpenClaw 对照**:
| Claude Code | OpenClaw |
|-------------|----------|
| `Agent(tool)` | `sessions_spawn` |
| `SendMessage` | `sessions_send` |
| `TaskStop` | `subagents(action=kill)` |
| Worker 白名单 | `agents.list[].allowedTools` |

**学习要点**:
- 协调器不应该有执行能力，只负责分发
- Worker 应该有明确的工具边界
- 任务通知通过 XML 格式传递

---

### 2. Bash Security（Bash 安全检查）

**文件**: `src/tools/BashTool/bashSecurity.ts` (1700+ 行)

**23 种安全检查模式**:

| ID | 检查项 | 说明 |
|----|-------|------|
| 1 | INCOMPLETE_COMMANDS | 不完整命令（以 tab/-/操作符开头） |
| 2 | JQ_SYSTEM_FUNCTION | jq 的 system() 函数 |
| 3 | JQ_FILE_ARGUMENTS | jq 的危险文件参数 |
| 4 | OBFUSCATED_FLAGS | 混淆标志（引号绕过） |
| 5 | SHELL_METACHARACTERS | Shell 元字符（;|&） |
| 6 | DANGEROUS_VARIABLES | 危险变量（重定向/管道中的 $VAR） |
| 7 | NEWLINES | 换行符注入 |
| 8 | DANGEROUS_PATTERNS_COMMAND_SUBSTITUTION | 命令替换（$() `` ${}） |
| 9 | DANGEROUS_PATTERNS_INPUT_REDIRECTION | 输入重定向（<） |
| 10 | DANGEROUS_PATTERNS_OUTPUT_REDIRECTION | 输出重定向（>） |
| 11 | IFS_INJECTION | IFS 变量注入 |
| 12 | GIT_COMMIT_SUBSTITUTION | Git commit 中的命令替换 |
| 13 | PROC_ENVIRON_ACCESS | /proc/*/environ 访问 |
| 14 | MALFORMED_TOKEN_INJECTION | 畸形令牌注入 |
| 15 | BACKSLASH_ESCAPED_WHITESPACE | 反斜杠转义空白 |
| 16 | BRACE_EXPANSION | 大括号扩展（{a,b}） |
| 17 | CONTROL_CHARACTERS | 控制字符 |
| 18 | UNICODE_WHITESPACE | Unicode 空白字符 |
| 19 | MID_WORD_HASH | 词中 # |
| 20 | ZSH_DANGEROUS_COMMANDS | Zsh 危险命令（zmodload 等） |
| 21 | BACKSLASH_ESCAPED_OPERATORS | 反斜杠转义操作符（\; \| \&） |
| 22 | COMMENT_QUOTE_DESYNC | 注释中的引号脱同步 |
| 23 | QUOTED_NEWLINE | 引号内的换行符 |

**OpenClaw 对照**:
| Claude Code | OpenClaw |
|-------------|----------|
| bashSecurity.ts | `exec-approvals` + `safeBins` |
| 23 种检查 | `strictInlineEval` + 路径检查 |

**学习要点**:
- 安全检查应该是分层的（早期快速检查 → 深度验证）
- 不同解析器（shell-quote vs bash）的行为差异可能导致漏洞
- 控制字符、Unicode 空白、注释内的引号都是攻击向量

---

### 3. Fork Subagent（子 Agent 分支）

**文件**: `src/tools/AgentTool/forkSubagent.ts`

**核心思想**:
- Fork 继承父级上下文和缓存
- 不需要重新传递背景信息
- 适合"一次性"任务

**关键设计**:
```typescript
// Fork vs Subagent 区别
// Fork: 继承上下文，共享缓存，无 subagent_type
// Subagent: 全新上下文，独立缓存，有 subagent_type

// Fork 的触发条件
const isFork = !subagent_type && !model
```

**OpenClaw 对照**:
| Claude Code Fork | OpenClaw |
|------------------|----------|
| `Agent({name, prompt})` | `sessions_spawn({task, runtime="subagent"})` |
| 继承上下文 | 自动继承父级 workspace |
| 共享缓存 | 模型决定 |

**学习要点**:
- Fork 的价值在于"不污染父级上下文"
- 适合研究类任务（输出不需要保留在主对话中）
- 不应该设置 `model` 参数（会失去缓存共享）

---

### 4. Prompt Caching（提示词缓存）

**文件**: `src/constants/systemPromptSections.ts`

**核心思想**:
- 静态内容缓存，动态内容按需计算
- 分区设计：cache_break vs cached
- 相同占位符确保前缀一致

**关键设计**:
```typescript
// 静态分区（缓存）
const STATIC_SECTIONS = [
  systemPromptSection('core_instructions', () => CORE_PROMPT),
  systemPromptSection('tool_schemas', () => TOOL_SCHEMAS),
]

// 动态分区（每次计算，可能破坏缓存）
const DYNAMIC_SECTIONS = [
  DANGEROUS_uncachedSystemPromptSection('mcp_status', getMcpStatus, 'MCP 连接状态变化'),
]
```

**OpenClaw 对照**:
| Claude Code | OpenClaw |
|-------------|----------|
| `systemPromptSection` | 配置文件注入 |
| 静态/动态分区 | 暂无明确分区 |
| 缓存清除 | `/clear` `/compact` |

**学习要点**:
- 缓存节省 30-50% 成本
- 动态内容应该尽量后置
- 前缀一致性是缓存命中的关键

---

### 5. Token Budget（Token 预算）

**文件**: `src/query/tokenBudget.ts`

**核心思想**:
- 设置 Token 预算阈值
- 达到阈值后自动停止或继续
- 收益递减检测

**关键设计**:
```typescript
// 预算检查
const COMPLETION_THRESHOLD = 0.9  // 90% 时停止
const DIMINISHING_THRESHOLD = 500 // 连续 3 次增量 < 500 则收益递减

function checkTokenBudget(tracker, budget, tokens) {
  if (tokens < budget * 0.9 && !isDiminishing) {
    return { action: 'continue', nudgeMessage: '...' }
  }
  return { action: 'stop', completionEvent: {...} }
}
```

**OpenClaw 对照**:
| Claude Code | OpenClaw |
|-------------|----------|
| `checkTokenBudget` | 暂无 |
| 收益递减检测 | 暂无 |

**学习要点**:
- 预算管理可以防止无限循环
- 收益递减检测可以智能终止
- Nudge 消息可以引导 Agent 完成

---

### 6. Agent Memory（Agent 记忆）

**文件**: `src/tools/AgentTool/agentMemory.ts`

**核心思想**:
- Agent 间共享记忆
- 快照机制
- 跨会话持久化

**OpenClaw 对照**:
| Claude Code | OpenClaw |
|-------------|----------|
| `agentMemory` | `memory_search` + `MEMORY.md` |
| 快照 | 暂无 |

---

## 实施优先级（修订）

| 优先级 | 模块 | OpenClaw 现状 | 学习行动 |
|-------|------|--------------|---------|
| 1 | Bash 安全 | ✅ 已有 `exec-approvals` | 研究 23 种检查模式，增强配置 |
| 2 | Fork Skill | ✅ 已有 `sessions_spawn` | 优化 Fork Skill 行为定义 |
| 3 | Coordinator | ✅ 已有 Multi-Agent | 学习系统提示词设计 |
| 4 | Prompt Caching | ⚠️ 部分 | 学习分区设计 |
| 5 | Token Budget | ❌ 无 | **值得新增** |
| 6 | Agent Memory | ⚠️ 部分 | 学习快照机制 |

---

## 可以直接借鉴的设计

### 1. Token Budget Hook

```typescript
// 为 OpenClaw 创建 Token Budget Hook
// ~/.openclaw/hooks/token-budget/handler.ts

const handler = async (event) => {
  if (event.type !== 'session' || event.action !== 'compact:before') {
    return
  }

  const { tokenCount, budget } = event.context
  if (tokenCount > budget * 0.9) {
    event.messages.push(`⚠️ Token 使用已达 ${Math.round(tokenCount/budget*100)}%`)
  }
}
```

### 2. Fork Skill 增强

```markdown
# 现有 Fork Skill 可以增加：
- 不设置 model（保持缓存共享）
- 简短 name（方便 UI 显示）
- 明确的 scope 边界
- 不 peek 中间结果
```

### 3. Bash 安全配置增强

```json
{
  "exec": {
    "strictInlineEval": true,
    "safeBins": ["head", "tail", "wc", "tr", "cut", "uniq"],
    "safeBinTrustedDirs": ["/bin", "/usr/bin"]
  }
}
```

---

## 源码保护

- **原始包**: `claude-code-2.1.88.tgz` 已备份
- **提取源码**: `restored-src/` 可随时查阅
- **Git 追踪**: 整个 sourcemap 目录在 workspace git 仓库中

---

*Created: 2026-03-31*
*Status: 深度学习中*
