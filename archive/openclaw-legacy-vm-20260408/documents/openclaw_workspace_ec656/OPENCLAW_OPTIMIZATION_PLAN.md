# OpenClaw 系统优化计划
## 基于 Claude Code 源码逆向分析的深度研究

---

## 一、架构对比分析

### 1.1 Claude Code 核心架构特点

| 特性 | 实现方式 | 价值 |
|------|----------|------|
| **QueryEngine 模式** | 单一类管理整个对话生命周期 | 状态一致性、可测试性 |
| **Coordinator Mode** | 多 Agent 协调模式 | 并行任务执行、职责分离 |
| **Skills 系统** | 多来源技能加载 + Frontmatter 元数据 | 可扩展性、声明式配置 |
| **权限分层** | PermissionMode + Rules + Classifier | 细粒度控制、安全性 |
| **Feature Flags** | 运行时功能开关 | 渐进发布、A/B 测试 |
| **工具权限白名单** | ASYNC_AGENT_ALLOWED_TOOLS | 安全边界、防止递归 |
| **Prompt Caching** | 静态/动态内容分离 + Cache Scope | 成本优化、响应速度 |

### 1.2 OpenClaw 现有架构

| 组件 | 现状 | 对比 Claude Code |
|------|------|------------------|
| Agent Runner | `runReplyAgent` 函数式 | 缺少 QueryEngine 类封装 |
| 工具系统 | `AnyAgentTool` + Profile 配置 | 缺少细粒度权限分类器 |
| Skills | 独立 Skills 目录 + 插件系统 | 可借鉴 Frontmatter 扩展 |
| 会话管理 | SessionEntry + SessionStore | 类似但缺少 Coordinator 模式 |
| 权限系统 | ownerOnly + 工具 Profile | 缺少 YOLO Classifier |

---

## 二、关键优化领域

### 🔴 P0 - 高优先级

#### 2.1 引入 QueryEngine 类模式

**现状问题：**
- OpenClaw 的 `runReplyAgent` 是函数式设计
- 状态散落在多个参数中
- 难以进行细粒度控制和测试

**Claude Code 方案：**
```typescript
class QueryEngine {
  private config: QueryEngineConfig;
  private mutableMessages: Message[];
  private abortController: AbortController;
  private permissionDenials: SDKPermissionDenial[];
  private totalUsage: NonNullableUsage;
  private readFileState: FileStateCache;
  
  async *submitMessage(prompt, options): AsyncGenerator<SDKMessage> {
    // 核心对话循环
  }
}
```

**OpenClaw 优化方案：**
```typescript
// 新建 src/agents/QueryEngine.ts
export class OpenClawQueryEngine {
  private sessionState: SessionState;
  private toolContext: ToolExecutionContext;
  private messageHistory: Message[];
  private usageTracker: UsageTracker;
  
  constructor(config: QueryEngineConfig) {
    this.sessionState = new SessionState(config.sessionEntry);
    this.toolContext = buildToolContext(config);
  }
  
  async *submitMessage(ctx: MsgContext): AsyncGenerator<ReplyPayload> {
    // 统一的消息处理循环
    yield* this.processUserMessage(ctx);
    yield* this.executeToolCalls(ctx);
    yield* this.generateReply(ctx);
  }
}
```

**收益：**
- 状态集中管理
- 易于添加 Hook 和中间件
- 支持流式生成和中断恢复

---

#### 2.2 实现 Coordinator Mode

**现状问题：**
- OpenClaw 缺少多 Agent 协调能力
- 子任务无法并行执行
- 缺少任务间通信机制

**Claude Code 方案核心：**
```typescript
// coordinatorMode.ts
export function getCoordinatorSystemPrompt(): string {
  return `You are a coordinator. Your job is to:
- Help the user achieve their goal
- Direct workers to research, implement and verify code changes
- Synthesize results and communicate with the user`;
}

// 工具权限
export const COORDINATOR_MODE_ALLOWED_TOOLS = new Set([
  AGENT_TOOL_NAME,
  TASK_STOP_TOOL_NAME,
  SEND_MESSAGE_TOOL_NAME,
  SYNTHETIC_OUTPUT_TOOL_NAME,
]);
```

**OpenClaw 优化方案：**

```typescript
// 新建 src/agents/coordinator/coordinatorMode.ts
export interface CoordinatorConfig {
  maxConcurrentWorkers: number;
  workerTimeoutMs: number;
  scratchpadDir?: string;
}

export class CoordinatorEngine {
  private workers: Map<string, WorkerAgent> = new Map();
  private messageQueue: PriorityQueue<WorkerMessage>;
  
  async spawnWorker(config: WorkerConfig): Promise<WorkerHandle> {
    const worker = await this.createWorker(config);
    this.workers.set(worker.id, worker);
    return worker;
  }
  
  async sendMessageToWorker(workerId: string, message: string): Promise<void> {
    // 继续现有 Worker
  }
  
  async stopWorker(workerId: string): Promise<void> {
    // 停止 Worker
  }
  
  getCoordinatorPrompt(): string {
    return `你是 OpenClaw 协调器。你的职责是：
- 分配任务给 Worker Agent
- 综合多个 Worker 的结果
- 与用户沟通进展

可用工具：
- Agent: 生成新的 Worker
- SendMessage: 继续现有 Worker
- TaskStop: 停止 Worker`;
  }
}
```

**收益：**
- 支持并行任务执行
- 研究、实现、验证阶段分离
- 更好的任务跟踪和报告

---

#### 2.3 实现 YOLO Classifier 权限分类器

**现状问题：**
- OpenClaw 的 Bash 工具依赖简单的 ownerOnly 标志
- 缺少智能命令安全判断
- 无法区分危险和安全的命令

**Claude Code 方案：**
```typescript
// yoloClassifier.ts (52KB)
export function classifyBashCommand(command: string): Classification {
  // 使用 LLM 分类命令安全性
  // 返回: safe | dangerous | needs_confirmation
}

// dangerousPatterns.ts
export const DANGEROUS_BASH_PATTERNS = [
  'python', 'node', 'ruby', 'perl', 'bash', 'sh',
  'curl', 'wget', 'eval', 'exec'
];
```

**OpenClaw 优化方案：**

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
  private llmClassifier: LLMClassifier;
  
  async classify(command: string, context: CommandContext): Promise<CommandClassification> {
    // 1. 规则引擎快速判断
    const ruleResult = this.patterns.match(command);
    if (ruleResult.confidence > 0.9) {
      return ruleResult;
    }
    
    // 2. LLM 深度分析
    return this.llmClassifier.classify(command, context);
  }
  
  // 危险模式检测
  private detectDangerousPatterns(command: string): PatternMatch[] {
    const patterns = [
      { regex: /\brm\s+-rf\b/, risk: 'critical', reason: '递归删除' },
      { regex: /\bsudo\b/, risk: 'high', reason: '提权执行' },
      { regex: />\s*\/dev\/(sda|hda|nvme)/, risk: 'critical', reason: '磁盘覆写' },
      { regex: /\bcurl\b.*\|\s*(ba)?sh/, risk: 'critical', reason: '远程脚本执行' },
      { regex: /\beval\b/, risk: 'high', reason: '动态代码执行' },
    ];
    // ...
  }
}

// 集成到 BashTool
export function createBashTool(opts: BashToolOptions): AnyAgentTool {
  const classifier = new BashCommandClassifier();
  
  return {
    name: 'Bash',
    async execute(params) {
      const classification = await classifier.classify(params.command, context);
      
      if (classification.suggestedAction === 'deny') {
        return failedTextResult(`命令被拒绝: ${classification.reasoning}`);
      }
      
      if (classification.suggestedAction === 'confirm' && !opts.autoApprove) {
        // 请求用户确认
        const approved = await requestConfirmation(params.command, classification);
        if (!approved) return failedTextResult('用户拒绝');
      }
      
      return executeCommand(params.command);
    }
  };
}
```

**收益：**
- 智能安全判断
- 减少不必要的确认
- 保护系统免受危险操作

---

### 🟠 P1 - 中优先级

#### 2.4 Skills 系统 Frontmatter 扩展

**现状问题：**
- OpenClaw Skills 缺少结构化元数据
- 无法指定工具白名单/黑名单
- 缺少 whenToUse 智能匹配

**Claude Code 方案：**
```yaml
---
name: commit
description: Create a git commit with staged changes
allowed-tools: [Bash, Read]
arguments: [message]
when_to_use: when user wants to commit changes
model: inherit
effort: high
hooks:
  PreToolUse:
    - match: "Bash(git*)"
      command: "echo 'Git operation detected'"
---
```

**OpenClaw 优化方案：**

```yaml
# skills/commit/SKILL.md
---
name: commit
description: Create a git commit with staged changes
version: 1.0.0

# 工具控制
allowed-tools:
  - Bash
  - Read
  - Write
disallowed-tools:
  - Agent
  - SendMessage

# 参数定义
arguments:
  - name: message
    type: string
    required: true
    description: Commit message
  - name: scope
    type: enum
    values: [staged, all, interactive]
    default: staged

# 触发条件
when_to_use: |
  - User asks to commit changes
  - User says "commit this"
  - User mentions git commit
  
# Agent 关联
agent: coding-agent
model: default
effort: high

# Hooks
hooks:
  pre_execute:
    - command: "git status --porcelain"
      capture: staged_files
  post_execute:
    - command: "git log -1 --oneline"
      capture: commit_hash
---
```

**实现：**

```typescript
// 扩展 src/skills/loadSkillsDir.ts
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
}

export function parseSkillFrontmatter(content: string): SkillFrontmatter {
  const frontmatter = extractFrontmatter(content);
  return {
    name: frontmatter.name,
    description: frontmatter.description,
    allowedTools: parseToolList(frontmatter['allowed-tools']),
    // ...
  };
}

// 智能技能匹配
export class SkillMatcher {
  async findMatchingSkills(context: SkillContext): Promise<SkillMatch[]> {
    const skills = await this.loadSkills();
    const matches: SkillMatch[] = [];
    
    for (const skill of skills) {
      if (skill.whenToUse) {
        const relevance = await this.llmMatcher.match(
          context.userMessage,
          skill.whenToUse
        );
        if (relevance > 0.7) {
          matches.push({ skill, relevance });
        }
      }
    }
    
    return matches.sort((a, b) => b.relevance - a.relevance);
  }
}
```

---

#### 2.5 实现工具权限分层系统

**现状问题：**
- OpenClaw 只有 ownerOnly 二元判断
- 缺少细粒度的工具访问控制
- 无法针对不同场景配置不同权限

**Claude Code 方案：**
```typescript
// constants/tools.ts
export const ASYNC_AGENT_ALLOWED_TOOLS = new Set([
  FILE_READ_TOOL_NAME,
  WEB_SEARCH_TOOL_NAME,
  GREP_TOOL_NAME,
  SHELL_TOOL_NAMES,
  FILE_EDIT_TOOL_NAME,
  FILE_WRITE_TOOL_NAME,
]);

export const ALL_AGENT_DISALLOWED_TOOLS = new Set([
  AGENT_TOOL_NAME,  // 防止递归
  TASK_OUTPUT_TOOL_NAME,
  ASK_USER_QUESTION_TOOL_NAME,
]);
```

**OpenClaw 优化方案：**

```typescript
// 新建 src/agents/tools/permissions.ts
export type PermissionLevel = 
  | 'owner'      // 只有 owner 可用
  | 'trusted'    // 信任的发送者可用
  | 'member'     // 群组成员可用
  | 'anyone';    // 任何人可用

export type PermissionContext = 'coordinator' | 'worker' | 'subagent' | 'main';

export interface ToolPermissionPolicy {
  toolId: string;
  defaultLevel: PermissionLevel;
  contextOverrides?: Partial<Record<PermissionContext, PermissionLevel>>;
  riskLevel?: 'low' | 'medium' | 'high' | 'critical';
  requiresConfirmation?: boolean | ((params: unknown) => boolean);
}

// 工具权限注册表
export const TOOL_PERMISSION_REGISTRY: ToolPermissionPolicy[] = [
  // 文件系统工具 - 高风险
  { toolId: 'Write', defaultLevel: 'owner', riskLevel: 'high', requiresConfirmation: true },
  { toolId: 'Edit', defaultLevel: 'owner', riskLevel: 'high', requiresConfirmation: true },
  { toolId: 'Read', defaultLevel: 'trusted', riskLevel: 'low' },
  
  // Shell 工具 - 高风险
  { toolId: 'Bash', defaultLevel: 'owner', riskLevel: 'critical', 
    requiresConfirmation: (params) => isDestructiveCommand(params.command) },
  
  // 通信工具 - 中风险
  { toolId: 'SendMessage', defaultLevel: 'trusted', riskLevel: 'medium' },
  
  // Agent 工具 - 特殊权限
  { toolId: 'Agent', defaultLevel: 'owner', riskLevel: 'high',
    contextOverrides: { worker: 'denied' } },  // Worker 不能创建子 Agent
  
  // 只读工具 - 低风险
  { toolId: 'WebSearch', defaultLevel: 'anyone', riskLevel: 'low' },
  { toolId: 'WebFetch', defaultLevel: 'anyone', riskLevel: 'low' },
];

// 权限检查器
export class ToolPermissionChecker {
  check(params: {
    toolId: string;
    context: PermissionContext;
    senderLevel: PermissionLevel;
    toolParams: unknown;
  }): PermissionDecision {
    const policy = this.getPolicy(params.toolId);
    const effectiveLevel = policy.contextOverrides?.[params.context] 
      ?? policy.defaultLevel;
    
    if (effectiveLevel === 'denied') {
      return { allowed: false, reason: 'Context denied' };
    }
    
    const levelOrder: PermissionLevel[] = ['anyone', 'member', 'trusted', 'owner'];
    const senderIndex = levelOrder.indexOf(params.senderLevel);
    const requiredIndex = levelOrder.indexOf(effectiveLevel);
    
    if (senderIndex < requiredIndex) {
      return { allowed: false, reason: `Requires ${effectiveLevel}` };
    }
    
    if (typeof policy.requiresConfirmation === 'function') {
      if (policy.requiresConfirmation(params.toolParams)) {
        return { allowed: true, needsConfirmation: true };
      }
    } else if (policy.requiresConfirmation) {
      return { allowed: true, needsConfirmation: true };
    }
    
    return { allowed: true };
  }
}
```

---

#### 2.6 实现 Prompt Caching 优化

**现状问题：**
- OpenClaw 未实现 Prompt Caching
- 每次请求都重新处理完整上下文
- 成本和延迟较高

**Claude Code 方案：**
```typescript
// api/claude.ts
export const SYSTEM_PROMPT_DYNAMIC_BOUNDARY = '__SYSTEM_PROMPT_DYNAMIC_BOUNDARY__';

// 静态内容使用 global cache scope
const staticBlocks = systemPrompt.slice(0, boundaryIndex);
const dynamicBlocks = systemPrompt.slice(boundaryIndex);

// 构建带 cache 标记的消息
function buildSystemPromptBlocks(prompts: SystemPrompt[]): ContentBlockParam[] {
  return prompts.map((prompt, index) => ({
    type: 'text',
    text: prompt.content,
    cache_control: index < boundaryIndex 
      ? { type: 'ephemeral', scope: 'global' }
      : { type: 'ephemeral' }
  }));
}
```

**OpenClaw 优化方案：**

```typescript
// 新建 src/agents/prompt/caching.ts
export const PROMPT_CACHE_BOUNDARY = '__CACHE_BOUNDARY__';

export type CacheScope = 'global' | 'user' | 'session';

export interface CacheablePrompt {
  content: string;
  scope: CacheScope;
  cacheKey: string;
}

// Prompt 分区
export class PromptPartitioner {
  partition(prompts: SystemPrompt[]): {
    static: CacheablePrompt[];   // 可全局缓存
    user: CacheablePrompt[];     // 用户级缓存
    session: CacheablePrompt[];  // 会话级缓存
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
    // 基于内容 hash 生成缓存 key
    return createHash('sha256').update(prompt.content).digest('hex');
  }
}

// API 请求构建
export function buildCachedRequest(params: {
  staticPrompts: CacheablePrompt[];
  userPrompts: CacheablePrompt[];
  sessionPrompts: CacheablePrompt[];
  messages: Message[];
}): APIRequest {
  const systemBlocks: ContentBlockParam[] = [];
  
  // 静态内容 - global cache
  for (const prompt of params.staticPrompts) {
    systemBlocks.push({
      type: 'text',
      text: prompt.content,
      cache_control: { type: 'ephemeral' }  // Anthropic API
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
  
  // 会话级内容
  for (const prompt of params.sessionPrompts) {
    systemBlocks.push({
      type: 'text',
      text: prompt.content
    });
  }
  
  return { system: systemBlocks, messages: params.messages };
}

// 缓存命中统计
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

### 🟡 P2 - 低优先级

#### 2.7 Feature Flags 系统

```typescript
// 新建 src/config/featureFlags.ts
export type FeatureFlag = 
  | 'COORDINATOR_MODE'
  | 'YOLO_CLASSIFIER'
  | 'PROMPT_CACHING'
  | 'SKILL_MATCHING'
  | 'PARALLEL_WORKERS';

export class FeatureFlagService {
  private flags: Map<FeatureFlag, boolean> = new Map();
  
  isEnabled(flag: FeatureFlag): boolean {
    // 1. 环境变量覆盖
    const envValue = process.env[`OPENCLAW_${flag}`];
    if (envValue !== undefined) {
      return envValue === 'true';
    }
    
    // 2. 配置文件
    // 3. 远程开关 (可选)
    return this.flags.get(flag) ?? false;
  }
  
  setFlag(flag: FeatureFlag, value: boolean): void {
    this.flags.set(flag, value);
  }
}

// 使用
if (featureFlags.isEnabled('COORDINATOR_MODE')) {
  engine = new CoordinatorEngine(config);
}
```

#### 2.8 会话恢复和快照

```typescript
// 基于 Claude Code 的 sessionRestore.ts
export interface SessionSnapshot {
  sessionId: string;
  messages: Message[];
  toolStates: Map<string, unknown>;
  createdAt: number;
  checksum: string;
}

export class SessionSnapshotManager {
  async createSnapshot(sessionKey: string): Promise<SessionSnapshot> {
    const session = await this.sessionStore.get(sessionKey);
    return {
      sessionId: sessionKey,
      messages: session.messages,
      toolStates: this.captureToolStates(session),
      createdAt: Date.now(),
      checksum: this.computeChecksum(session)
    };
  }
  
  async restoreSnapshot(snapshot: SessionSnapshot): Promise<void> {
    await this.sessionStore.set(snapshot.sessionId, {
      messages: snapshot.messages,
      toolStates: snapshot.toolStates
    });
  }
}
```

---

## 三、实施路线图

### Phase 1: 基础重构 (Week 1-2)

```
✅ 创建 QueryEngine 类框架
✅ 重构 runReplyAgent 为类方法
✅ 添加状态管理基础设施
```

### Phase 2: 权限系统 (Week 3-4)

```
✅ 实现 ToolPermissionRegistry
✅ 集成 BashCommandClassifier
✅ 添加权限检查中间件
```

### Phase 3: 协调器模式 (Week 5-6)

```
✅ 实现 CoordinatorEngine
✅ 添加 Worker 生命周期管理
✅ 实现消息传递机制
```

### Phase 4: 性能优化 (Week 7-8)

```
✅ 实现 Prompt Caching
✅ 添加缓存统计
✅ 性能基准测试
```

### Phase 5: Skills 增强 (Week 9-10)

```
✅ 扩展 Frontmatter 解析
✅ 实现智能技能匹配
✅ 添加 Hooks 系统
```

---

## 四、关键代码示例

### 4.1 QueryEngine 核心实现

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

### 4.2 Coordinator 模式实现

```typescript
// src/agents/coordinator/CoordinatorEngine.ts
export class CoordinatorEngine {
  private workers: Map<string, WorkerHandle> = new Map();
  private messageQueue: MessageQueue;
  private scratchpad: ScratchpadManager;
  
  constructor(private config: CoordinatorConfig) {
    this.messageQueue = new MessageQueue();
    this.scratchpad = new ScratchpadManager(config.scratchpadDir);
  }
  
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
    if (!worker) {
      throw new Error(`Worker ${workerId} not found`);
    }
    
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
- 每条消息给 Worker 必须自包含所有上下文

${this.scratchpad.isAvailable() ? `
Scratchpad 目录: ${this.scratchpad.path}
Worker 可以在此目录读写共享信息。
` : ''}`;
  }
  
  private filterWorkerTools(allowedTools?: string[]): Map<string, AnyAgentTool> {
    const workerAllowedTools = new Set([
      'Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob',
      'WebSearch', 'WebFetch', 'Skill'
    ]);
    
    if (allowedTools) {
      allowedTools.forEach(t => workerAllowedTools.add(t));
    }
    
    // 禁止的工具
    const disallowed = new Set(['Agent', 'SendMessage', 'TaskStop']);
    
    return new Map(
      [...this.config.tools.entries()]
        .filter(([name]) => workerAllowedTools.has(name) && !disallowed.has(name))
    );
  }
}
```

---

## 五、测试策略

### 5.1 单元测试

```typescript
// __tests__/agents/QueryEngine.test.ts
describe('OpenClawQueryEngine', () => {
  it('should process message and return reply', async () => {
    const engine = new OpenClawQueryEngine(mockConfig);
    const replies = [];
    
    for await (const reply of engine.processMessage(mockCtx)) {
      replies.push(reply);
    }
    
    expect(replies).toContainEqual(
      expect.objectContaining({ type: 'text' })
    );
  });
  
  it('should deny tool without permission', async () => {
    const engine = new OpenClawQueryEngine({
      ...mockConfig,
      senderLevel: 'member'
    });
    
    // ... 测试权限拒绝
  });
  
  it('should handle abort gracefully', async () => {
    const engine = new OpenClawQueryEngine(mockConfig);
    
    const promise = collectReplies(engine.processMessage(mockCtx));
    engine.abort();
    
    const replies = await promise;
    expect(replies).toContainEqual(
      expect.objectContaining({ type: 'aborted' })
    );
  });
});
```

### 5.2 集成测试

```typescript
// __tests__/agents/coordinator/CoordinatorEngine.test.ts
describe('CoordinatorEngine', () => {
  it('should spawn and manage workers', async () => {
    const coordinator = new CoordinatorEngine(mockConfig);
    
    const worker = await coordinator.spawnWorker({
      task: 'research',
      allowedTools: ['Read', 'Grep', 'WebSearch']
    });
    
    expect(worker.id).toBeDefined();
    expect(coordinator.workers.size).toBe(1);
    
    await coordinator.stopWorker(worker.id);
    expect(coordinator.workers.size).toBe(0);
  });
  
  it('should handle parallel workers', async () => {
    const coordinator = new CoordinatorEngine(mockConfig);
    
    const workers = await Promise.all([
      coordinator.spawnWorker({ task: 'research-1' }),
      coordinator.spawnWorker({ task: 'research-2' }),
      coordinator.spawnWorker({ task: 'research-3' })
    ]);
    
    expect(workers.length).toBe(3);
  });
});
```

---

## 六、监控和可观测性

### 6.1 指标收集

```typescript
// src/agents/metrics.ts
export class AgentMetrics {
  private histogram = new Map<string, number[]>();
  
  recordLatency(operation: string, durationMs: number): void {
    const samples = this.histogram.get(operation) ?? [];
    samples.push(durationMs);
    this.histogram.set(operation, samples);
  }
  
  recordToolExecution(tool: string, success: boolean): void {
    // 发送到监控系统
  }
  
  recordCacheHit(hit: boolean): void {
    // 缓存统计
  }
  
  getMetrics(): AgentMetricsReport {
    return {
      latencies: Object.fromEntries(this.histogram),
      toolExecutions: this.getToolStats(),
      cacheStats: this.getCacheStats()
    };
  }
}
```

---

## 七、总结

本优化计划基于对 Claude Code v2.1.88 源码的深度逆向分析，提炼出以下核心改进方向：

| 改进项 | 预期收益 | 实施复杂度 |
|--------|----------|------------|
| QueryEngine 类模式 | 状态一致性、可测试性 | 中 |
| Coordinator Mode | 并行任务执行 | 高 |
| 权限分类器 | 智能安全控制 | 中 |
| Skills Frontmatter | 可扩展性 | 低 |
| Prompt Caching | 成本降低 30-50% | 中 |
| Feature Flags | 渐进发布 | 低 |

**建议实施顺序：**
1. 先实施 QueryEngine 和权限系统（基础）
2. 再实施 Prompt Caching（快速见效）
3. 最后实施 Coordinator Mode（高级功能）

---

*Generated: 2026-03-31*
*Based on: Claude Code v2.1.88 Source Map Analysis*
