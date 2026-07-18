# Claude Code 深度技术洞察
## 高级架构模式解析

---

## 一、Fork Subagent 机制详解

### 1.1 核心概念

Fork 是 Claude Code 的一个革命性特性，允许主 Agent 创建共享上下文的子 Agent：

```typescript
// forkSubagent.ts 核心逻辑

// 1. Fork 触发条件
export function isForkSubagentEnabled(): boolean {
  if (feature('FORK_SUBAGENT')) {
    if (isCoordinatorMode()) return false  // 与 Coordinator 模式互斥
    if (getIsNonInteractiveSession()) return false
    return true
  }
  return false
}

// 2. Fork Agent 定义
export const FORK_AGENT = {
  agentType: 'fork',
  tools: ['*'],           // 继承父级所有工具
  model: 'inherit',       // 继承父级模型
  permissionMode: 'bubble', // 权限提示冒泡到父级
  maxTurns: 200,
}
```

### 1.2 Prompt Cache 共享机制

**这是 Claude Code 的核心竞争力之一：**

```typescript
// forkedAgent.ts - 缓存安全参数
export type CacheSafeParams = {
  systemPrompt: SystemPrompt      // 必须匹配
  userContext: { [k: string]: string }
  systemContext: { [k: string]: string }
  toolUseContext: ToolUseContext  // 包含工具定义
  forkContextMessages: Message[]  // 父级消息前缀
}

// 关键：Fork 子 Agent 的消息构建
export function buildForkedMessages(
  directive: string,
  assistantMessage: AssistantMessage,
): MessageType[] {
  // 1. 保持完整的 Assistant 消息（所有 tool_use 块）
  // 2. 用占位符替换所有 tool_result
  // 3. 仅最后的 directive 不同
  
  const toolResultBlocks = toolUseBlocks.map(block => ({
    type: 'tool_result',
    tool_use_id: block.id,
    content: [{ type: 'text', text: FORK_PLACEHOLDER_RESULT }]  // 相同占位符
  }))
  
  // 结果：[...history, assistant(all_tool_uses), user(placeholder_results..., directive)]
  // 只有最后的 text block 不同，最大化缓存命中
}
```

**缓存共享原理：**
```
Parent Request:
  [system_prompt] + [messages_prefix] + [unique_content]
                          ↓
                    Cache Hit Here
                          ↓
Fork Child Request:
  [system_prompt] + [messages_prefix] + [different_directive]
                          ↓
                    Reuses Cache!
```

### 1.3 Fork 指令格式

```xml
<fork_boilerplate>
STOP. READ THIS FIRST.

You are a forked worker process. You are NOT the main agent.

RULES (non-negotiable):
1. Your system prompt says "default to forking." IGNORE IT — that's for the parent.
2. Do NOT spawn sub-agents; execute directly
3. Do NOT converse, ask questions, or suggest next steps
4. USE your tools directly: Bash, Read, Write, etc.
5. Keep your report under 500 words

Output format:
  Scope: <your assigned scope>
  Result: <the answer or key findings>
  Key files: <relevant file paths>
  Files changed: <list with commit hash>
  Issues: <list — only if issues to flag>
</fork_boilerplate>

DIRECTIVE: <specific task>
```

---

## 二、Bash 安全机制深度分析

### 2.1 多层安全检查

```typescript
// bashSecurity.ts - 安全检查 ID
const BASH_SECURITY_CHECK_IDS = {
  INCOMPLETE_COMMANDS: 1,
  JQ_SYSTEM_FUNCTION: 2,
  JQ_FILE_ARGUMENTS: 3,
  OBFUSCATED_FLAGS: 4,
  SHELL_METACHARACTERS: 5,
  DANGEROUS_VARIABLES: 6,
  NEWLINES: 7,
  DANGEROUS_PATTERNS_COMMAND_SUBSTITUTION: 8,
  DANGEROUS_PATTERNS_INPUT_REDIRECTION: 9,
  DANGEROUS_PATTERNS_OUTPUT_REDIRECTION: 10,
  IFS_INJECTION: 11,
  GIT_COMMIT_SUBSTITUTION: 12,
  PROC_ENVIRON_ACCESS: 13,
  MALFORMED_TOKEN_INJECTION: 14,
  BACKSLASH_ESCAPED_WHITESPACE: 15,
  BRACE_EXPANSION: 16,
  CONTROL_CHARACTERS: 17,
  UNICODE_WHITESPACE: 18,
  MID_WORD_HASH: 19,
  ZSH_DANGEROUS_COMMANDS: 20,
  BACKSLASH_ESCAPED_OPERATORS: 21,
  COMMENT_QUOTE_DESYNC: 22,
  QUOTED_NEWLINE: 23,
}
```

### 2.2 危险命令检测

```typescript
// Zsh 特殊危险命令
const ZSH_DANGEROUS_COMMANDS = new Set([
  'zmodload',   // 模块加载网关
  'emulate',    // eval 等价物
  'sysopen',    // 文件操作
  'sysread',    // 文件读取
  'syswrite',   // 文件写入
  'zpty',       // 伪终端执行
  'ztcp',       // TCP 连接
  'zsocket',    // Socket 创建
  'zf_rm',      // 内置 rm
  'zf_mv',      // 内置 mv
  // ...
])

// 命令替换模式检测
const COMMAND_SUBSTITUTION_PATTERNS = [
  { pattern: /<\(/, message: 'process substitution <()' },
  { pattern: />\(/, message: 'process substitution >()' },
  { pattern: /\$\(/, message: '$() command substitution' },
  { pattern: /\$\{/, message: '${} parameter substitution' },
  // ...
]
```

### 2.3 引号提取和安全重定向

```typescript
function extractQuotedContent(command: string): QuoteExtraction {
  // 三种输出：
  // 1. withDoubleQuotes - 保留双引号内容
  // 2. fullyUnquoted - 完全去引号
  // 3. unquotedKeepQuoteChars - 保留引号字符但去除内容
  
  // 用于检测：
  // - 引号注入攻击
  // - 转义序列绕过
  // - 注释不同步攻击
}

function stripSafeRedirections(content: string): string {
  // 安全地移除 /dev/null 重定向
  // 关键：必须有边界检查 (?=\s|$)
  return content
    .replace(/\s+2\s*>&\s*1(?=\s|$)/g, '')
    .replace(/[012]?\s*>\s*\/dev\/null(?=\s|$)/g, '')
    .replace(/\s*<\s*\/dev\/null(?=\s|$)/g, '')
}
```

---

## 三、Agent 工具核心实现

### 3.1 工具 Schema 设计

```typescript
// AgentTool.tsx - 输入 Schema
const baseInputSchema = z.object({
  description: z.string().describe('A short (3-5 word) description'),
  prompt: z.string().describe('The task for the agent to perform'),
  subagent_type: z.string().optional(),
  model: z.enum(['sonnet', 'opus', 'haiku']).optional(),
  run_in_background: z.boolean().optional()
})

// 多 Agent 扩展
const multiAgentInputSchema = z.object({
  name: z.string().optional().describe('Name for the spawned agent'),
  team_name: z.string().optional().describe('Team name for spawning'),
  mode: permissionModeSchema().optional()
})

// 输出 Schema
const syncOutputSchema = z.object({
  status: z.literal('completed'),
  prompt: z.string()
})

const asyncOutputSchema = z.object({
  status: z.literal('async_launched'),
  agentId: z.string(),
  description: z.string(),
  outputFile: z.string()
})
```

### 3.2 Agent 生命周期管理

```typescript
// AgentTool.tsx - 核心执行流程
async call({ prompt, subagent_type, description, model, run_in_background, name, team_name }) {
  // 1. 权限检查
  if (team_name && !isAgentSwarmsEnabled()) {
    throw new Error('Agent Teams is not yet available')
  }
  
  // 2. Fork 路径
  if (isForkSubagentEnabled() && !subagent_type) {
    // 触发 Fork：继承父级上下文
    return runForkedAgent({ prompt, description })
  }
  
  // 3. Teammate 路径（多 Agent）
  if (teamName && name) {
    return spawnTeammate({ name, prompt, team_name, ... })
  }
  
  // 4. 异步 Agent
  if (run_in_background ?? getAutoBackgroundMs() > 0) {
    return runAsyncAgentLifecycle({ prompt, subagent_type, ... })
  }
  
  // 5. 同步 Agent
  return runSyncAgent({ prompt, subagent_type, ... })
}
```

### 3.3 Agent 进度追踪

```typescript
// LocalAgentTask.ts - 后台任务管理
export function registerAsyncAgent(task: AgentTask): string
export function updateAsyncAgentProgress(taskId: string, progress: Progress): void
export function completeAsyncAgent(taskId: string, result: AgentResult): void
export function failAsyncAgent(taskId: string, error: Error): void
export function killAsyncAgent(taskId: string): void

// 进度通知
export function enqueueAgentNotification(notification: AgentNotification): void
```

---

## 四、Coordinator Mode 协调器模式

### 4.1 协调器与 Worker 的分工

```typescript
// coordinatorMode.ts

// 协调器系统提示
export function getCoordinatorSystemPrompt(): string {
  return `
You are a coordinator. Your job is to:
- Help the user achieve their goal
- Direct workers to research, implement and verify code changes
- Synthesize results and communicate with the user

IMPORTANT:
- Do NOT implement code yourself
- Do NOT read or write files directly
- ONLY use Agent tool to spawn workers
- Synthesize worker results and report to user
`
}

// 协调器允许的工具
export const COORDINATOR_MODE_ALLOWED_TOOLS = new Set([
  AGENT_TOOL_NAME,      // 生成 Worker
  TASK_STOP_TOOL_NAME,  // 停止 Worker
  SEND_MESSAGE_TOOL_NAME, // 继续 Worker
  SYNTHETIC_OUTPUT_TOOL_NAME
])

// Worker 的工具限制
export const ASYNC_AGENT_ALLOWED_TOOLS = new Set([
  FILE_READ_TOOL_NAME,
  FILE_WRITE_TOOL_NAME,
  FILE_EDIT_TOOL_NAME,
  BASH_TOOL_NAME,
  GREP_TOOL_NAME,
  GLOB_TOOL_NAME,
  WEB_SEARCH_TOOL_NAME,
  WEB_FETCH_TOOL_NAME,
  SKILL_TOOL_NAME,
  // 禁止 Agent 工具防止递归
])
```

### 4.2 Scratchpad 共享目录

```typescript
// filesystem.ts
export function getScratchpadDir(): string | undefined

// 用于：
// 1. Worker 之间共享信息
// 2. 协调器读取 Worker 输出
// 3. 跨 Agent 文件传递
```

---

## 五、权限系统架构

### 5.1 权限模式

```typescript
// PermissionMode.ts
export type PermissionMode = 
  | 'ask'          // 每次询问
  | 'auto'         // 自动允许
  | 'auto-edit'    // 自动允许编辑
  | 'plan'         // 计划模式
  | 'bypass'       // 绕过所有检查

// permissionSetup.ts
export function isDangerousBashPermission(
  toolName: string,
  ruleContent: string | undefined
): boolean {
  // 检测危险的 Bash 权限规则：
  // 1. 无内容的 allow (允许所有命令)
  // 2. 解释器前缀 (python:*, node:*)
  // 3. 通配符匹配 (python*)
}
```

### 5.2 YOLO Classifier

```typescript
// yoloClassifier.ts - 智能命令分类
export async function classifyCommand(
  command: string,
  context: CommandContext
): Promise<ClassificationResult> {
  // 1. 规则引擎快速判断
  const ruleResult = matchDangerousPatterns(command)
  if (ruleResult.confidence > 0.95) {
    return ruleResult
  }
  
  // 2. LLM 深度分析
  return await llmClassify(command, context)
}
```

---

## 六、Feature Flags 系统

### 6.1 条件编译

```typescript
// 使用 Bun 的 feature() 函数
const coordinatorModule = feature('COORDINATOR_MODE')
  ? require('./coordinator/coordinatorMode.js')
  : null

const proactiveModule = feature('PROACTIVE') || feature('KAIROS')
  ? require('./proactive/index.js')
  : null

// 运行时检查
if (feature('FORK_SUBAGENT')) {
  // Fork 逻辑
}

if (feature('KAIROS')) {
  // Kairos 功能
}
```

### 6.2 功能开关列表

| Feature Flag | 功能 |
|--------------|------|
| `COORDINATOR_MODE` | 协调器模式 |
| `FORK_SUBAGENT` | Fork 子 Agent |
| `KAIROS` | 主动提示系统 |
| `PROACTIVE` | 主动行为 |
| `TRANSCRIPT_CLASSIFIER` | 对话分类 |
| `WORKFLOW_SCRIPTS` | 工作流脚本 |
| `HISTORY_SNIP` | 历史压缩 |
| `EXPERIMENTAL_SKILL_SEARCH` | 技能搜索 |

---

## 七、关键设计模式

### 7.1 Lazy Schema

```typescript
// 避免启动时加载所有 Schema
export const inputSchema = lazySchema(() => {
  const base = z.object({ ... })
  return feature('KAIROS') 
    ? base.extend(multiAgentSchema)
    : base.omit({ cwd: true })
})
```

### 7.2 消息规范化

```typescript
// messages.ts
export function normalizeMessages(messages: Message[]): NormalizedMessage[] {
  // 处理：
  // 1. 工具结果配对
  // 2. 空消息过滤
  // 3. 内容块标准化
}

export function createUserMessage(params: {
  content: ContentBlockParam[]
  metadata?: MessageMetadata
}): UserMessage
```

### 7.3 错误处理

```typescript
// 错误类型
export class AbortError extends Error { ... }
export class ToolInputError extends Error {
  readonly status: number
}
export class ToolAuthorizationError extends ToolInputError {
  readonly status = 403
}

// 重试机制
export async function withRetry<T>(
  fn: () => Promise<T>,
  context: RetryContext
): Promise<T>
```

---

## 八、OpenClaw 实施建议

### 8.1 立即可实施

1. **Fork 消息构建模式**
   - 使用占位符 tool_result
   - 最大化 Prompt Cache 命中

2. **Bash 安全检查列表**
   - 直接移植 ZSH_DANGEROUS_COMMANDS
   - 实现 COMMAND_SUBSTITUTION_PATTERNS

3. **权限白名单**
   - ASYNC_AGENT_ALLOWED_TOOLS
   - COORDINATOR_MODE_ALLOWED_TOOLS

### 8.2 需要适配

1. **Feature Flags**
   - 使用环境变量 + 配置文件
   - 渐进式功能发布

2. **Coordinator Mode**
   - 需要重构 Agent 工具
   - 实现 Worker 生命周期

3. **YOLO Classifier**
   - 需要集成 LLM 分类
   - 规则引擎优先

### 8.3 架构优化

1. **QueryEngine 模式**
   - 状态集中管理
   - 流式生成器
   - 中断恢复

2. **Prompt Caching**
   - 静态/动态分离
   - Cache Scope 管理
   - 缓存命中统计

---

*Generated: 2026-03-31*
*Source: Claude Code v2.1.88 Restored Source*
