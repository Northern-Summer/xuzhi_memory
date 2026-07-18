# Claude Code 深度融合研究报告
## 工程设计精要与 OpenClaw 融合方案

---

## 前言：研究方法论

本文档基于对 Claude Code v2.1.88 源码的逐行深度阅读，而非表面浏览。研究方法：

1. **逐模块精读** - 阅读完整源文件，而非仅看接口
2. **理解设计决策** - 追踪注释中的历史原因和权衡
3. **交叉验证** - 对比多个相关文件，确认架构一致性
4. **提取可迁移模式** - 识别与具体业务无关的通用设计

---

## 一、核心架构：QueryEngine 模式

### 1.1 设计洞察

```typescript
// Claude Code 的 QueryEngine 核心结构
export class QueryEngine {
  private config: QueryEngineConfig;
  private mutableMessages: Message[];       // 状态集中
  private abortController: AbortController; // 中断控制
  private permissionDenials: SDKPermissionDenial[]; // 权限追踪
  private totalUsage: NonNullableUsage;     // Token 统计
  private readFileState: FileStateCache;    // 文件缓存
  
  async *submitMessage(prompt, options): AsyncGenerator<SDKMessage> {
    // 1. 预处理 - 系统提示构建、权限上下文
    // 2. 消息处理 - 用户输入解析、附件处理
    // 3. 查询循环 - LLM 调用、工具执行
    // 4. 后处理 - 结果标准化、状态持久化
  }
}
```

**关键设计决策**：

| 设计 | 原因 | 价值 |
|------|------|------|
| 状态集中管理 | 避免散落在多个参数中 | 可测试、可中断、可恢复 |
| AsyncGenerator | 流式输出 + 中断支持 | 用户体验 + 资源控制 |
| FileStateCache | 避免重复读取 | 性能优化 |
| permissionDenials 追踪 | SDK 需要报告被拒绝的操作 | 可观测性 |

### 1.2 OpenClaw 现状对比

```typescript
// OpenClaw 的 runReplyAgent 是函数式设计
export async function runReplyAgent(ctx: ReplyContext): Promise<void> {
  // 状态散落在 ctx 的多个属性中
  // 难以进行细粒度控制和测试
}
```

**问题**：
1. 状态分散，难以追踪
2. 无法优雅中断
3. 缺少统一的生命周期管理

### 1.3 融合方案

**原则**：不破坏现有功能，渐进式重构

```typescript
// 新建 src/agents/QueryEngine.ts
export class OpenClawQueryEngine {
  // 1. 保留现有 runReplyAgent 的核心逻辑
  // 2. 添加状态管理基础设施
  // 3. 实现 AsyncGenerator 接口
  
  private sessionState: SessionState;
  private messageHistory: Message[];
  private usageTracker: UsageTracker;
  private abortController: AbortController;
  
  async *processMessage(ctx: MsgContext): AsyncGenerator<ReplyPayload> {
    // Phase 1: 预处理
    const processedInput = await this.preprocessInput(ctx);
    yield { type: 'status', status: 'processing' };
    
    // Phase 2: 查询循环
    while (!this.state.isComplete) {
      const response = await this.queryLLM(processedInput);
      yield* this.streamResponse(response);
      
      if (response.toolCalls.length > 0) {
        yield* this.executeToolCalls(response.toolCalls, ctx);
      }
      
      if (this.shouldTerminate(response)) {
        this.state.isComplete = true;
      }
    }
    
    // Phase 3: 后处理
    yield* this.postprocess(ctx);
  }
  
  abort(): void {
    this.abortController.abort();
  }
}
```

**迁移路径**：
1. 创建 QueryEngine 类，内部调用现有 runReplyAgent
2. 新功能使用 QueryEngine，旧功能保持不变
3. 逐步迁移现有代码

---

## 二、Fork Subagent 机制

### 2.1 设计洞察

```typescript
// forkSubagent.ts 核心逻辑

/** 占位符文本 - 所有 fork 子 Agent 共享，实现 Prompt Cache 命中 */
const FORK_PLACEHOLDER_RESULT = 'Fork started — processing in background';

export function buildForkedMessages(
  directive: string,
  assistantMessage: AssistantMessage,
): MessageType[] {
  // 1. 保留完整的父级 assistant 消息（所有 tool_use 块）
  // 2. 构建单个 user 消息，包含：
  //    - 所有 tool_result 块使用相同的占位符
  //    - 追加一个 per-child 指令文本块
  
  // 结果: [...history, assistant(all_tool_uses), user(placeholder_results..., directive)]
  // 只有最后的文本块不同，最大化 Cache 命中
}
```

**关键设计决策**：

| 设计 | 原因 | 价值 |
|------|------|------|
| 相同占位符 | 所有 fork 子 Agent 产生相同的 API 请求前缀 | Prompt Cache 命中 |
| 保留完整 tool_use | 不修改父级消息结构 | 状态一致性 |
| per-child 指令 | 唯一差异化的部分 | 任务特定化 |

### 2.2 Fork 子 Agent 的系统提示

```typescript
export function buildChildMessage(directive: string): string {
  return `<${FORK_BOILERPLATE_TAG}>
STOP. READ THIS FIRST.

You are a forked worker process. You are NOT the main agent.

RULES (non-negotiable):
1. Your system prompt says "default to forking." IGNORE IT — that's for the parent. 
   You ARE the fork. Do NOT spawn sub-agents; execute directly.
2. Do NOT converse, ask questions, or suggest next steps
3. Do NOT editorialize or add meta-commentary
4. USE your tools directly: Bash, Read, Write, etc.
5. If you modify files, commit your changes before reporting...
6. Do NOT emit text between tool calls. Use tools silently, then report once at the end.
7. Stay strictly within your directive's scope...
8. Keep your report under 500 words...
9. Your response MUST begin with "Scope:". No preamble...
10. REPORT structured facts, then stop

Output format:
  Scope: <echo back your assigned scope>
  Result: <the answer or key findings>
  Key files: <relevant file paths>
  Files changed: <list with commit hash>
  Issues: <list>
</${FORK_BOILERPLATE_TAG}>

${FORK_DIRECTIVE_PREFIX}${directive}`;
}
```

**精妙之处**：
1. **自反性处理** - 告诉子 Agent 忽略"默认 fork"指令，防止递归
2. **行为约束** - 10 条非协商规则，确保输出一致性
3. **结构化输出** - 固定格式，便于解析和聚合

### 2.3 OpenClaw 融合方案

```typescript
// 新建 src/agents/fork.ts

export const FORK_PLACEHOLDER_RESULT = 'Fork started — processing in background';

export interface ForkConfig {
  parentMessages: Message[];
  directive: string;
  inheritTools: boolean;
  permissionMode: 'bubble' | 'inherit';
}

export class ForkSubagentEngine {
  buildForkedMessages(config: ForkConfig): Message[] {
    const lastAssistant = this.getLastAssistantMessage(config.parentMessages);
    
    // 1. 保留完整 assistant 消息
    const fullAssistant = this.cloneAssistantMessage(lastAssistant);
    
    // 2. 构建 tool_result 占位符
    const toolResults = this.buildPlaceholderResults(lastAssistant);
    
    // 3. 追加指令
    const directiveBlock = this.buildDirectiveBlock(config.directive);
    
    return [
      fullAssistant,
      createUserMessage({ content: [...toolResults, directiveBlock] })
    ];
  }
  
  private buildDirectiveBlock(directive: string): ContentBlock {
    return {
      type: 'text',
      text: this.buildForkSystemPrompt(directive)
    };
  }
}
```

**关键实现要点**：
1. **Prompt Cache 优化** - 确保所有 fork 子 Agent 使用相同的占位符
2. **权限冒泡** - 子 Agent 的权限请求传递给父级
3. **递归防护** - 检测 fork boilerplate 标签，防止嵌套

---

## 三、Coordinator Mode（协调器模式）

### 3.1 设计洞察

```typescript
// coordinatorMode.ts 核心逻辑

export function getCoordinatorSystemPrompt(): string {
  return `You are Claude Code, an AI assistant that orchestrates software engineering tasks across multiple workers.

## 1. Your Role

You are a **coordinator**. Your job is to:
- Help the user achieve their goal
- Direct workers to research, implement and verify code changes
- Synthesize results and communicate with the user
- Answer questions directly when possible

Every message you send is to the user. Worker results and system notifications are internal signals — never thank or acknowledge them.

## 2. Your Tools

- **Agent** - Spawn a new worker
- **SendMessage** - Continue an existing worker
- **TaskStop** - Stop a running worker

## 3. Workers

Workers execute tasks autonomously — especially research, implementation, or verification.

## 4. Task Workflow

| Phase | Who | Purpose |
|-------|-----|---------|
| Research | Workers (parallel) | Investigate codebase |
| Synthesis | **You** (coordinator) | Read findings, craft specs |
| Implementation | Workers | Make targeted changes |
| Verification | Workers | Test changes work |

## 5. Writing Worker Prompts

**Workers can't see your conversation.** Every prompt must be self-contained.

### Always synthesize — your most important job

Never write "based on your findings" — these phrases delegate understanding to the worker instead of doing it yourself.

// Good — synthesized spec
Agent({ prompt: "Fix the null pointer in src/auth/validate.ts:42. The user field can be undefined when the session expires. Add a null check and return early with an appropriate error. Commit and report the hash." })

// Bad — lazy delegation
Agent({ prompt: "Based on your findings, implement the fix" })
`;
}
```

**关键设计决策**：

| 设计 | 原因 | 价值 |
|------|------|------|
| Coordinator 不执行工具 | 专注协调，避免上下文污染 | 清晰职责分离 |
| Workers 不能看 Coordinator 对话 | 每个提示自包含 | 可靠的任务传递 |
| 必须综合（synthesize） | 防止懒惰委托 | 高质量任务规格 |
| 并行执行 | Workers 是异步的 | 效率最大化 |

### 3.2 工具权限分层

```typescript
// constants/tools.ts

// Coordinator 可用的工具
export const COORDINATOR_MODE_ALLOWED_TOOLS = new Set([
  AGENT_TOOL_NAME,      // 生成 Worker
  TASK_STOP_TOOL_NAME,  // 停止 Worker
  SEND_MESSAGE_TOOL_NAME, // 继续 Worker
  SYNTHETIC_OUTPUT_TOOL_NAME, // 结构化输出
]);

// Worker 可用的工具（异步 Agent）
export const ASYNC_AGENT_ALLOWED_TOOLS = new Set([
  FILE_READ_TOOL_NAME,
  WEB_SEARCH_TOOL_NAME,
  GREP_TOOL_NAME,
  SHELL_TOOL_NAMES,
  FILE_EDIT_TOOL_NAME,
  FILE_WRITE_TOOL_NAME,
  SKILL_TOOL_NAME,
  // ... 无 Agent 工具，防止递归
]);

// 所有 Agent 禁止的工具
export const ALL_AGENT_DISALLOWED_TOOLS = new Set([
  AGENT_TOOL_NAME,      // 防止递归
  TASK_OUTPUT_TOOL_NAME,
  ASK_USER_QUESTION_TOOL_NAME,
  TASK_STOP_TOOL_NAME,
]);
```

### 3.3 OpenClaw 融合方案

```typescript
// 新建 src/agents/coordinator/CoordinatorEngine.ts

export class CoordinatorEngine {
  private workers: Map<string, WorkerHandle> = new Map();
  private messageQueue: PriorityQueue<WorkerMessage>;
  private scratchpad: ScratchpadManager;
  
  async spawnWorker(config: WorkerConfig): Promise<WorkerHandle> {
    const id = generateWorkerId();
    
    // 创建隔离的 QueryEngine
    const engine = new OpenClawQueryEngine({
      sessionId: `${this.config.sessionId}:worker:${id}`,
      tools: this.filterWorkerTools(config.allowedTools),
      context: 'worker',
      parentEngine: this
    });
    
    const worker: WorkerHandle = {
      id,
      engine,
      status: 'idle',
      createdAt: Date.now()
    };
    
    this.workers.set(id, worker);
    this.emit('worker_spawned', { workerId: id });
    
    return worker;
  }
  
  async sendMessageToWorker(workerId: string, message: string): Promise<void> {
    const worker = this.workers.get(workerId);
    if (!worker) throw new Error(`Worker ${workerId} not found`);
    
    await this.messageQueue.enqueue({
      workerId,
      message,
      timestamp: Date.now()
    });
  }
  
  async stopWorker(workerId: string): Promise<void> {
    const worker = this.workers.get(workerId);
    if (!worker) return;
    
    worker.engine.abort();
    worker.status = 'stopped';
    this.workers.delete(workerId);
    
    this.emit('worker_stopped', { workerId });
  }
  
  getCoordinatorPrompt(): string {
    return `你是 OpenClaw 协调器。

你的职责：
- 理解用户目标并分解为可执行任务
- 分配任务给 Worker Agent（使用 Agent 工具）
- 综合多个 Worker 的结果
- 与用户沟通进展

可用工具：
- Agent: 生成新的 Worker 处理子任务
- SendMessage: 继续现有 Worker 的任务
- TaskStop: 停止正在运行的 Worker

工作流程：
1. Research: 启动多个 Worker 并行调研
2. Synthesis: 分析调研结果，制定实现方案
3. Implementation: 指派 Worker 执行实现
4. Verification: 验证实现正确性

重要原则：
- 并行执行独立任务
- 不要预测 Worker 结果
- Worker 完成后会自动通知你
- 每条消息给 Worker 必须自包含所有上下文`;
  }
  
  private filterWorkerTools(allowedTools?: string[]): Map<string, AnyAgentTool> {
    const workerAllowedTools = new Set([
      'Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob',
      'WebSearch', 'WebFetch', 'Skill'
    ]);
    
    if (allowedTools) {
      allowedTools.forEach(t => workerAllowedTools.add(t));
    }
    
    // 禁止的工具 - 防止递归
    const disallowed = new Set(['Agent', 'SendMessage', 'TaskStop']);
    
    return new Map(
      [...this.config.tools.entries()]
        .filter(([name]) => workerAllowedTools.has(name) && !disallowed.has(name))
    );
  }
}
```

---

## 四、Bash 安全系统

### 4.1 设计洞察

```typescript
// bashSecurity.ts (102KB) - 核心安全检查

// 23 种安全检查 ID
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
};

// Zsh 危险命令
const ZSH_DANGEROUS_COMMANDS = new Set([
  'zmodload',  // 模块加载网关
  'emulate',   // eval 等价物
  'sysopen', 'sysread', 'syswrite', 'sysseek', // 文件描述符操作
  'zpty',      // 伪终端执行
  'ztcp',      // TCP 连接
  'zsocket',   // Unix/TCP socket
  'zf_rm', 'zf_mv', 'zf_ln', 'zf_chmod', // 内置文件操作
]);

// 命令替换模式检测
const COMMAND_SUBSTITUTION_PATTERNS = [
  { pattern: /<\(/, message: 'process substitution <()' },
  { pattern: />\(/, message: 'process substitution >()' },
  { pattern: /=\(/, message: 'Zsh process substitution =()' },
  { pattern: /(?:^|[\s;&|])=[a-zA-Z_]/, message: 'Zsh equals expansion (=cmd)' },
  { pattern: /\$\(/, message: '$() command substitution' },
  { pattern: /\$\{/, message: '${} parameter substitution' },
  // ...
];
```

**关键设计决策**：

| 设计 | 原因 | 价值 |
|------|------|------|
| 数字 ID 而非字符串 | 避免在日志中暴露敏感信息 | 安全性 |
| 多层验证 | 纵深防御 | 多重保障 |
| Zsh 特殊处理 | Zsh 有独特的危险特性 | 完整覆盖 |
| Tree-sitter 解析 | 比 regex 更准确 | 精确检测 |

### 4.2 引号提取算法

```typescript
function extractQuotedContent(command: string, isJq = false): QuoteExtraction {
  let withDoubleQuotes = '';
  let fullyUnquoted = '';
  let unquotedKeepQuoteChars = '';
  let inSingleQuote = false;
  let inDoubleQuote = false;
  let escaped = false;

  for (let i = 0; i < command.length; i++) {
    const char = command[i];

    if (escaped) {
      escaped = false;
      if (!inSingleQuote) withDoubleQuotes += char;
      if (!inSingleQuote && !inDoubleQuote) fullyUnquoted += char;
      if (!inSingleQuote && !inDoubleQuote) unquotedKeepQuoteChars += char;
      continue;
    }

    if (char === '\\' && !inSingleQuote) {
      escaped = true;
      // ... 处理转义
      continue;
    }

    if (char === "'" && !inDoubleQuote) {
      inSingleQuote = !inSingleQuote;
      unquotedKeepQuoteChars += char;
      continue;
    }

    if (char === '"' && !inSingleQuote) {
      inDoubleQuote = !inDoubleQuote;
      unquotedKeepQuoteChars += char;
      continue;
    }

    // ... 收集字符
  }

  return { withDoubleQuotes, fullyUnquoted, unquotedKeepQuoteChars };
}
```

**精妙之处**：
1. **三种输出** - 满足不同检测需求
2. **正确处理转义** - 区分 `\` 和 `\\`
3. **保留引号字符** - 用于检测引号相邻的特殊情况

### 4.3 OpenClaw 融合方案

```typescript
// 新建 src/agents/tools/bash/security.ts

export const BASH_SECURITY_CHECK_IDS = {
  // 移植全部 23 种
};

export const ZSH_DANGEROUS_COMMANDS = new Set([
  // 移植全部命令
]);

export const COMMAND_SUBSTITUTION_PATTERNS = [
  // 移植全部模式
];

export class BashSecurityChecker {
  private treeSitter?: TreeSitterAnalyzer;
  
  async validate(command: string): Promise<SecurityResult> {
    const context = this.buildValidationContext(command);
    
    // 按顺序执行所有检查
    const checks = [
      this.validateEmpty,
      this.validateIncompleteCommands,
      this.validateJqSystemFunction,
      this.validateJqFileArguments,
      this.validateObfuscatedFlags,
      this.validateShellMetacharacters,
      this.validateDangerousVariables,
      this.validateNewlines,
      this.validateDangerousPatterns,
      this.validateIFSInjection,
      this.validateGitCommitSubstitution,
      this.validateProcEnvironAccess,
      this.validateMalformedTokenInjection,
      this.validateBackslashEscapedWhitespace,
      this.validateBraceExpansion,
      this.validateControlCharacters,
      this.validateUnicodeWhitespace,
      this.validateMidWordHash,
      this.validateZshDangerousCommands,
      this.validateBackslashEscapedOperators,
      this.validateCommentQuoteDesync,
      this.validateQuotedNewline,
    ];
    
    for (const check of checks) {
      const result = await check.call(this, context);
      if (result.behavior !== 'passthrough') {
        return result;
      }
    }
    
    return { behavior: 'allow', decisionReason: { type: 'other', reason: 'All checks passed' } };
  }
  
  private buildValidationContext(command: string): ValidationContext {
    const { withDoubleQuotes, fullyUnquoted, unquotedKeepQuoteChars } = 
      extractQuotedContent(command);
    
    return {
      originalCommand: command,
      baseCommand: this.extractBaseCommand(fullyUnquoted),
      unquotedContent: withDoubleQuotes,
      fullyUnquotedContent: stripSafeRedirections(fullyUnquoted),
      fullyUnquotedPreStrip: fullyUnquoted,
      unquotedKeepQuoteChars,
      treeSitter: this.treeSitter?.parse(command),
    };
  }
}
```

---

## 五、YOLO Classifier（权限分类器）

### 5.1 设计洞察

```typescript
// yoloClassifier.ts (52KB) - LLM 辅助权限判断

export async function classifyBashPermission(params: {
  command: string,
  permissionContext: ToolPermissionContext,
  messages: Message[],
}): Promise<PermissionResult> {
  // 1. 规则引擎快速判断
  const ruleResult = checkPermissionRules(params);
  if (ruleResult.confidence > 0.9) {
    return ruleResult;
  }
  
  // 2. LLM 深度分析
  const classifierResult = await runClassifierLLM(params);
  return classifierResult;
}

// Auto Mode 权限模板
const BASE_PROMPT = `You are a permission classifier. Your job is to determine whether a command should be:
- allowed (auto-approve)
- denied (auto-reject)
- needs_confirmation (ask user)

<permissions_template>
<user_allow_rules_to_replace>
- Read files in the current project
- Run tests
- Format code
- Git status, diff, log
</user_allow_rules_to_replace>

<user_deny_rules_to_replace>
- Delete files without confirmation
- Modify system configuration
- Install packages globally
- Push to protected branches
</user_deny_rules_to_replace>

<user_environment_to_replace>
- Project directory: /home/user/project
- Git repository: yes
- Node.js project: yes
</user_environment_to_replace>
</permissions_template>
`;
```

**关键设计决策**：

| 设计 | 原因 | 价值 |
|------|------|------|
| 规则 + LLM 双层 | 规则快速，LLM 精确 | 效率 + 准确性 |
| 可配置规则 | 不同项目有不同需求 | 灵活性 |
| 结构化输出 | 便于程序处理 | 可靠性 |

### 5.2 OpenClaw 融合方案

```typescript
// 新建 src/agents/tools/bash/classifier.ts

export type CommandRisk = 'safe' | 'low' | 'medium' | 'high' | 'critical';

export interface CommandClassification {
  risk: CommandRisk;
  confidence: number;
  reasoning?: string;
  suggestedAction: 'allow' | 'confirm' | 'deny';
}

export class BashCommandClassifier {
  private patterns: DangerousPatternRegistry;
  private llmClassifier?: LLMClassifier;
  
  async classify(command: string, context: CommandContext): Promise<CommandClassification> {
    // 1. 规则引擎快速判断
    const ruleResult = this.patterns.match(command);
    if (ruleResult.confidence > 0.9) {
      return ruleResult;
    }
    
    // 2. 安全检查器验证
    const securityResult = await this.securityChecker.validate(command);
    if (securityResult.behavior !== 'allow') {
      return {
        risk: 'high',
        confidence: 0.95,
        reasoning: securityResult.message,
        suggestedAction: securityResult.behavior === 'ask' ? 'confirm' : 'deny',
      };
    }
    
    // 3. LLM 深度分析（可选）
    if (this.llmClassifier && ruleResult.confidence < 0.7) {
      return this.llmClassifier.classify(command, context);
    }
    
    // 4. 默认需要确认
    return {
      risk: 'medium',
      confidence: 0.5,
      suggestedAction: 'confirm',
    };
  }
  
  private detectDangerousPatterns(command: string): PatternMatch[] {
    const patterns = [
      { regex: /\brm\s+-rf\b/, risk: 'critical', reason: '递归删除' },
      { regex: /\bsudo\b/, risk: 'high', reason: '提权执行' },
      { regex: />\s*\/dev\/(sda|hda|nvme)/, risk: 'critical', reason: '磁盘覆写' },
      { regex: /\bcurl\b.*\|\s*(ba)?sh/, risk: 'critical', reason: '远程脚本执行' },
      { regex: /\beval\b/, risk: 'high', reason: '动态代码执行' },
    ];
    
    return patterns
      .filter(p => p.regex.test(command))
      .map(p => ({ risk: p.risk, reason: p.reason }));
  }
}
```

---

## 六、Prompt Caching

### 6.1 设计洞察

```typescript
// api/claude.ts - Prompt Caching 实现

export const SYSTEM_PROMPT_DYNAMIC_BOUNDARY = '__SYSTEM_PROMPT_DYNAMIC_BOUNDARY__';

export function buildCachedRequest(params: {
  staticPrompts: SystemPrompt[];
  userPrompts: SystemPrompt[];
  sessionPrompts: SystemPrompt[];
  messages: Message[];
}): APIRequest {
  const systemBlocks: ContentBlockParam[] = [];
  
  // 静态内容 - global cache scope
  for (const prompt of params.staticPrompts) {
    systemBlocks.push({
      type: 'text',
      text: prompt.content,
      cache_control: { type: 'ephemeral' }
    });
  }
  
  // 用户级内容
  for (const prompt of params.userPrompts) {
    systemBlocks.push({
      type: 'text',
      text: prompt.content,
      cache_control: { type: 'ephemeral' }
    });
  }
  
  // 会话级内容 - 不缓存
  for (const prompt of params.sessionPrompts) {
    systemBlocks.push({
      type: 'text',
      text: prompt.content
    });
  }
  
  return { system: systemBlocks, messages: params.messages };
}
```

**关键设计决策**：

| 设计 | 原因 | 价值 |
|------|------|------|
| 静态/动态分离 | 静态内容可全局缓存 | Cache 命中率 |
| 边界标记 | 明确区分缓存范围 | 可维护性 |
| Scope 分层 | global/user/session | 精细化控制 |

### 6.2 OpenClaw 融合方案

```typescript
// 新建 src/agents/prompt/caching.ts

export const PROMPT_CACHE_BOUNDARY = '__CACHE_BOUNDARY__';

export type CacheScope = 'global' | 'user' | 'session';

export interface CacheablePrompt {
  content: string;
  scope: CacheScope;
  cacheKey: string;
}

export class PromptPartitioner {
  partition(prompts: SystemPrompt[]): {
    static: CacheablePrompt[];
    user: CacheablePrompt[];
    session: CacheablePrompt[];
  } {
    return {
      static: prompts.filter(p => p.isStatic).map(p => ({
        content: p.content,
        scope: 'global' as const,
        cacheKey: this.computeCacheKey(p)
      })),
      user: prompts.filter(p => p.isUserLevel).map(p => ({
        content: p.content,
        scope: 'user' as const,
        cacheKey: this.computeCacheKey(p)
      })),
      session: prompts.filter(p => p.isSessionLevel).map(p => ({
        content: p.content,
        scope: 'session' as const,
        cacheKey: this.computeCacheKey(p)
      }))
    };
  }
  
  private computeCacheKey(prompt: SystemPrompt): string {
    return createHash('sha256').update(prompt.content).digest('hex');
  }
}

// 缓存统计
export class CacheStatistics {
  private hits = 0;
  private misses = 0;
  
  recordHit() { this.hits++; }
  recordMiss() { this.misses++; }
  
  getStats() {
    return {
      hits: this.hits,
      misses: this.misses,
      hitRate: this.hits / (this.hits + this.misses)
    };
  }
}
```

---

## 七、Skills 系统

### 7.1 设计洞察

```typescript
// loadSkillsDir.ts - Skills 加载

export interface SkillFrontmatter {
  name: string;
  description: string;
  version?: string;
  allowedTools?: string[];
  disallowedTools?: string[];
  arguments?: SkillArgument[];
  whenToUse?: string;
  agent?: string;
  model?: string;
  effort?: 'low' | 'medium' | 'high';
  hooks?: SkillHooks;
  paths?: string[];  // 条件激活路径
}

// 条件技能激活
export function activateConditionalSkillsForPaths(
  filePaths: string[],
  cwd: string,
): string[] {
  for (const [name, skill] of conditionalSkills) {
    const skillIgnore = ignore().add(skill.paths);
    for (const filePath of filePaths) {
      const relativePath = relative(cwd, filePath);
      if (skillIgnore.ignores(relativePath)) {
        // 激活此技能
        dynamicSkills.set(name, skill);
        conditionalSkills.delete(name);
        activatedConditionalSkillNames.add(name);
        break;
      }
    }
  }
}
```

**关键设计决策**：

| 设计 | 原因 | 价值 |
|------|------|------|
| 目录格式 | skill-name/SKILL.md | 清晰组织 |
| Frontmatter 元数据 | 声明式配置 | 可扩展性 |
| 条件激活 | paths 前缀匹配 | 按需加载 |
| 多来源加载 | managed/user/project/plugin | 灵活性 |

### 7.2 OpenClaw 融合方案

OpenClaw 已有 Skills 系统，需要扩展：

```yaml
# skills/example/SKILL.md
---
name: example
description: Example skill
version: 1.0.0

# 扩展字段
allowed-tools:
  - Bash
  - Read
  - Write
disallowed-tools:
  - Agent

# 参数定义
arguments:
  - name: target
    type: string
    required: true
    description: Target file or directory

# 触发条件
when_to_use: |
  - User asks to example something
  - User mentions "example this"

# Agent 关联
agent: coding-agent
model: default
effort: high

# 条件激活
paths:
  - "src/**/*.ts"
  - "lib/**/*.js"

# Hooks
hooks:
  pre_execute:
    - command: "echo 'Starting...'"
  post_execute:
    - command: "echo 'Done!'"
---

# Skill content here...
```

---

## 八、Hooks 系统

### 8.1 设计洞察

```typescript
// hooks.ts (159KB) - 生命周期钩子

export type HookEvent =
  | 'PreToolUse'
  | 'PostToolUse'
  | 'PreCompact'
  | 'PostCompact'
  | 'SessionStart'
  | 'SessionEnd'
  | 'Stop'
  | 'SubagentStart'
  | 'SubagentStop'
  | 'TeammateIdle'
  | 'TaskCreated'
  | 'TaskCompleted'
  | 'ConfigChange'
  | 'CwdChanged'
  | 'FileChanged'
  | 'InstructionsLoaded'
  | 'UserPromptSubmit'
  | 'PermissionRequest'
  | 'Elicitation'
  | 'ElicitationResult';

export interface HookInput {
  event: HookEvent;
  session_id: string;
  transcript_path: string;
  cwd: string;
  // ... 事件特定字段
}

export interface HookOutput {
  status: 'success' | 'error' | 'blocking';
  message?: string;
  reason?: string;
  // ... 输出字段
}
```

**关键设计决策**：

| 设计 | 原因 | 价值 |
|------|------|------|
| 丰富的事件类型 | 覆盖整个生命周期 | 可扩展性 |
| JSON 输入输出 | 便于程序处理 | 标准化 |
| 异步支持 | 长时间运行的钩子 | 灵活性 |
| 信任检查 | 安全边界 | 安全性 |

### 8.2 OpenClaw 融合方案

```typescript
// 扩展现有 Hooks 系统

export type OpenClawHookEvent = 
  | 'PreToolUse'
  | 'PostToolUse'
  | 'PreSession'
  | 'PostSession'
  | 'PreCompact'
  | 'PostCompact'
  | 'UserPromptSubmit'
  | 'PermissionRequest'
  // 新增事件
  | 'ForkStart'
  | 'ForkComplete'
  | 'WorkerSpawn'
  | 'WorkerComplete'
  | 'CoordinatorDecision';

export interface HookExecutor {
  execute(input: HookInput): Promise<HookOutput>;
}

export class HookManager {
  private hooks: Map<HookEvent, HookExecutor[]> = new Map();
  
  register(event: HookEvent, executor: HookExecutor): void {
    const executors = this.hooks.get(event) ?? [];
    executors.push(executor);
    this.hooks.set(event, executors);
  }
  
  async fire(event: HookEvent, input: HookInput): Promise<HookOutput[]> {
    const executors = this.hooks.get(event) ?? [];
    const results: HookOutput[] = [];
    
    for (const executor of executors) {
      const result = await executor.execute(input);
      results.push(result);
      
      // 阻塞型钩子停止执行
      if (result.status === 'blocking') {
        break;
      }
    }
    
    return results;
  }
}
```

---

## 九、融合路线图

### Phase 1: 基础重构（Week 1-2）

**目标**：建立核心架构

```
┌─────────────────────────────────────────────────────────────┐
│                     OpenClaw QueryEngine                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ SessionState│  │ UsageTracker│  │ AbortController     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                      processMessage()                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│  │Preprocess│→ │Query Loop│→ │Tool Exec │→ │Postprocess│  │
│  └──────────┘  └──────────┘  └──────────┘  └───────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**任务清单**：
- [ ] 创建 `src/agents/QueryEngine.ts`
- [ ] 实现 `EngineState` 状态管理
- [ ] 重构 `runReplyAgent` 为类方法
- [ ] 添加 `abort()` 中断机制
- [ ] 单元测试覆盖

### Phase 2: 安全系统（Week 3-4）

**目标**：移植 Bash 安全检查

```
┌─────────────────────────────────────────────────────────────┐
│                    Bash Security System                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐                                        │
│  │ SecurityChecker │                                        │
│  └────────┬────────┘                                        │
│           │                                                 │
│  ┌────────▼────────┐  ┌─────────────────┐                  │
│  │ 23 Validators   │  │ PatternRegistry │                  │
│  └─────────────────┘  └─────────────────┘                  │
│           │                                                 │
│  ┌────────▼────────┐                                        │
│  │ CommandClassifier│                                       │
│  └────────┬────────┘                                        │
│           │                                                 │
│  ┌────────▼────────┐                                        │
│  │ PermissionResult│                                        │
│  └─────────────────┘                                        │
└─────────────────────────────────────────────────────────────┘
```

**任务清单**：
- [ ] 移植 `ZSH_DANGEROUS_COMMANDS`
- [ ] 移植 `COMMAND_SUBSTITUTION_PATTERNS`
- [ ] 实现 `extractQuotedContent()`
- [ ] 实现 `stripSafeRedirections()`
- [ ] 添加 23 种安全检查
- [ ] 集成到 BashTool

### Phase 3: Agent 系统（Week 5-6）

**目标**：实现 Fork 和 Coordinator 模式

```
┌─────────────────────────────────────────────────────────────┐
│                      Coordinator Mode                        │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐                                           │
│  │ Coordinator  │                                           │
│  │   Engine     │                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
│    ┌────▼────┐                                              │
│    │ Workers │                                              │
│    └────┬────┘                                              │
│         │                                                    │
│  ┌──────▼──────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Fork Engine │  │ Worker Pool  │  │ Scratchpad   │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

**任务清单**：
- [ ] 实现 `ForkSubagentEngine`
- [ ] 实现 `CoordinatorEngine`
- [ ] 添加 Worker 生命周期管理
- [ ] 实现消息传递机制
- [ ] 添加 Scratchpad 共享

### Phase 4: 性能优化（Week 7-8）

**目标**：实现 Prompt Caching

```
┌─────────────────────────────────────────────────────────────┐
│                    Prompt Caching System                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐                                        │
│  │ PromptPartitioner│                                       │
│  └────────┬────────┘                                        │
│           │                                                 │
│  ┌────────▼────────┐                                        │
│  │ static/user/    │                                        │
│  │ session prompts │                                        │
│  └────────┬────────┘                                        │
│           │                                                 │
│  ┌────────▼────────┐                                        │
│  │ CachedRequest   │                                        │
│  │ Builder         │                                        │
│  └────────┬────────┘                                        │
│           │                                                 │
│  ┌────────▼────────┐                                        │
│  │ CacheStatistics │                                        │
│  └─────────────────┘                                        │
└─────────────────────────────────────────────────────────────┘
```

**任务清单**：
- [ ] 实现 `PromptPartitioner`
- [ ] 实现 `buildCachedRequest()`
- [ ] 添加缓存统计
- [ ] 性能基准测试

### Phase 5: 技能增强（Week 9-10）

**目标**：扩展 Skills 和 Hooks

**任务清单**：
- [ ] 扩展 Frontmatter 解析
- [ ] 实现条件激活
- [ ] 添加 Hooks 系统
- [ ] 智能技能匹配

---

## 十、关键代码示例

### 10.1 完整的 QueryEngine 实现

```typescript
// src/agents/QueryEngine.ts

export class OpenClawQueryEngine {
  private state: EngineState;
  private tools: Map<string, AnyAgentTool>;
  private permissionChecker: ToolPermissionChecker;
  private abortController: AbortController;
  
  constructor(private config: QueryEngineConfig) {
    this.state = new EngineState(config.sessionEntry);
    this.tools = this.buildToolRegistry(config);
    this.permissionChecker = new ToolPermissionChecker();
    this.abortController = new AbortController();
  }
  
  async *processMessage(ctx: MsgContext): AsyncGenerator<ReplyPayload> {
    try {
      // 1. 预处理
      const processedInput = await this.preprocessInput(ctx);
      yield { type: 'status', status: 'processing' };
      
      // 2. 工具调用循环
      while (!this.state.isComplete) {
        const response = await this.queryLLM(processedInput);
        
        // 流式输出
        yield* this.streamResponse(response);
        
        // 执行工具调用
        if (response.toolCalls.length > 0) {
          yield* this.executeToolCalls(response.toolCalls, ctx);
        }
        
        // 检查终止条件
        if (this.shouldTerminate(response)) {
          this.state.isComplete = true;
        }
      }
      
      // 3. 后处理
      yield* this.postprocess(ctx);
      
    } catch (error) {
      if (error instanceof AbortError) {
        yield { type: 'aborted', reason: 'User aborted' };
      } else {
        yield { type: 'error', error: error.message };
      }
    }
  }
  
  private async *executeToolCalls(
    calls: ToolCall[], 
    ctx: MsgContext
  ): AsyncGenerator<ReplyPayload> {
    for (const call of calls) {
      // 权限检查
      const decision = this.permissionChecker.check({
        toolId: call.name,
        context: this.state.context,
        senderLevel: ctx.senderLevel,
        toolParams: call.params
      });
      
      if (!decision.allowed) {
        yield { type: 'tool_denied', tool: call.name, reason: decision.reason };
        continue;
      }
      
      if (decision.needsConfirmation) {
        const confirmed = await this.requestConfirmation(call, ctx);
        if (!confirmed) {
          yield { type: 'tool_denied', tool: call.name, reason: 'User rejected' };
          continue;
        }
      }
      
      // 执行工具
      const tool = this.tools.get(call.name);
      if (!tool) {
        yield { type: 'tool_error', tool: call.name, error: 'Tool not found' };
        continue;
      }
      
      yield { type: 'tool_start', tool: call.name };
      
      const result = await tool.execute(call.params, this.buildToolContext(ctx));
      
      yield { type: 'tool_result', tool: call.name, result };
      
      this.state.addToolResult(call.id, result);
    }
  }
  
  abort(): void {
    this.abortController.abort();
  }
}
```

### 10.2 完整的 Fork 实现

```typescript
// src/agents/fork.ts

export class ForkSubagentEngine {
  private static PLACEHOLDER = 'Fork started — processing in background';
  
  buildForkedMessages(config: ForkConfig): Message[] {
    const lastAssistant = this.getLastAssistantMessage(config.parentMessages);
    
    // 1. 保留完整 assistant 消息
    const fullAssistant: AssistantMessage = {
      ...lastAssistant,
      uuid: randomUUID(),
      message: {
        ...lastAssistant.message,
        content: [...lastAssistant.message.content]
      }
    };
    
    // 2. 收集所有 tool_use 块
    const toolUseBlocks = lastAssistant.message.content.filter(
      (block): block is ToolUseBlock => block.type === 'tool_use'
    );
    
    // 3. 构建占位符 tool_result
    const toolResultBlocks = toolUseBlocks.map(block => ({
      type: 'tool_result' as const,
      tool_use_id: block.id,
      content: [{ type: 'text' as const, text: ForkSubagentEngine.PLACEHOLDER }]
    }));
    
    // 4. 构建指令块
    const directiveBlock = {
      type: 'text' as const,
      text: this.buildForkDirective(config.directive)
    };
    
    // 5. 构建 user 消息
    const toolResultMessage = createUserMessage({
      content: [...toolResultBlocks, directiveBlock]
    });
    
    return [fullAssistant, toolResultMessage];
  }
  
  private buildForkDirective(directive: string): string {
    return `<fork-boilerplate>
STOP. READ THIS FIRST.

You are a forked worker process. You are NOT the main agent.

RULES (non-negotiable):
1. Do NOT spawn sub-agents; execute directly.
2. Do NOT converse or ask questions.
3. USE your tools directly: Bash, Read, Write, etc.
4. Keep your report under 500 words.
5. Your response MUST begin with "Scope:".

Output format:
  Scope: <your assigned scope>
  Result: <key findings>
  Key files: <relevant paths>
  Files changed: <with commit hash>
  Issues: <list if any>
</fork-boilerplate>

DIRECTIVE: ${directive}`;
  }
  
  isInForkChild(messages: Message[]): boolean {
    return messages.some(m => {
      if (m.type !== 'user') return false;
      const content = m.message.content;
      if (!Array.isArray(content)) return false;
      return content.some(
        block => block.type === 'text' && block.text.includes('<fork-boilerplate>')
      );
    });
  }
}
```

---

## 十一、总结

### 核心收获

| 模块 | 关键洞察 | 融合优先级 |
|------|----------|------------|
| QueryEngine | 状态集中 + AsyncGenerator | P0 |
| Fork | 相同占位符 → Cache 命中 | P0 |
| Coordinator | 综合而非委托 | P1 |
| Bash Security | 23 种检查 + Zsh 特殊处理 | P0 |
| YOLO Classifier | 规则 + LLM 双层 | P1 |
| Prompt Caching | 静态/动态分离 | P1 |
| Skills | Frontmatter + 条件激活 | P2 |
| Hooks | 生命周期全覆盖 | P2 |

### 设计原则

1. **渐进式重构** - 不破坏现有功能
2. **模块化设计** - 高内聚，低耦合
3. **测试驱动** - 每个模块都有单元测试
4. **文档先行** - 设计文档在代码之前

### 下一步行动

1. **深入验证** - 对比 OpenClaw 现有实现，确认差异
2. **原型开发** - 先实现 QueryEngine，验证架构
3. **逐步迁移** - 按模块逐步迁移，保持系统稳定

---

*Generated: 2026-03-31*
*Status: 深度研究完成，待融合实施*
