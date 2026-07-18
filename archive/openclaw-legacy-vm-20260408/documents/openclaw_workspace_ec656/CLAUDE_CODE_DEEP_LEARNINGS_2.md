# Claude Code 源码深度学习笔记（续）

## 新发现模块

### 7. Compact 系统

**文件**: `src/services/compact/`

**核心文件**:
- `compact.ts` (1700+ 行) — 核心压缩逻辑
- `prompt.ts` — 压缩提示词设计
- `microCompact.ts` — 微压缩
- `autoCompact.ts` — 自动压缩

**关键设计**:

```typescript
// 压缩提示词结构
const BASE_COMPACT_PROMPT = `
1. Primary Request and Intent: 用户明确请求
2. Key Technical Concepts: 技术概念
3. Files and Code Sections: 文件和代码
4. Errors and fixes: 错误和修复
5. Problem Solving: 问题解决
6. All user messages: 所有用户消息
7. Pending Tasks: 待办任务
8. Current Work: 当前工作
9. Optional Next Step: 下一步
```

**OpenClaw 对照**:
| Claude Code | OpenClaw |
|-------------|----------|
| `compact.ts` | `session:compact:before/after` hooks |
| 微压缩 | 暂无 |
| 自动压缩 | 暂无 |

**学习要点**:
- 压缩应该保留关键决策和上下文
- 用户消息是理解意图的关键
- 下一步建议需要基于最近工作

---

### 8. Permission 系统

**文件**: `src/utils/permissions/`

**核心文件**:
- `permissions.ts` (1400+ 行) — 权限核心
- `PermissionResult.ts` — 权限结果类型
- `PermissionRule.ts` — 权限规则
- `yoloClassifier.ts` — 自动批准分类器
- `bashClassifier.ts` — Bash 命令分类器

**关键设计**:

```typescript
// 权限决策类型
type PermissionDecision<Input> = {
  behavior: 'allow' | 'deny' | 'ask'
  updatedInput?: Input      // 修改后的输入
  decisionReason?: {
    type: 'config' | 'classifier' | 'user'
    classifier?: 'auto-mode' | 'bash'
    reason: string
  }
}

// 权限拒绝追踪（防止暴力破解）
const DENIAL_LIMITS = {
  maxDenials: 3,
  cooldownMs: 60000
}
```

**OpenClaw 对照**:
| Claude Code | OpenClaw |
|-------------|----------|
| `PermissionResult` | `exec-approvals` |
| `yoloClassifier` | 暂无 |
| `denialTracking` | 暂无 |

**学习要点**:
- 权限决策应该是可解释的
- 分类器可以自动批准安全操作
- 拒绝追踪可以防止暴力破解

---

### 9. MCP 服务

**文件**: `src/services/mcp/`

**核心文件**:
- `MCPConnectionManager.tsx` — 连接管理
- `client.ts` — MCP 客户端
- `types.ts` — 类型定义
- `elicitationHandler.ts` — 请求处理

**OpenClaw 对照**:
| Claude Code | OpenClaw |
|-------------|----------|
| `MCPConnectionManager` | `mcp` 配置 |
| `elicitationHandler` | 暂无 |

---

### 10. State 管理

**文件**: `src/state/`

**核心文件**:
- `AppStateStore.ts` — 状态存储
- `store.ts` — 状态创建
- `selectors.ts` — 状态选择器

**关键设计**:

```typescript
// 状态结构
type AppState = {
  toolPermissionContext: ToolPermissionContext
  speculationState: SpeculationState
  // ...
}

// 状态变更回调
type OnChangeAppState = (args: {
  newState: AppState
  oldState: AppState
}) => void
```

---

### 11. Migrations 系统

**文件**: `src/migrations/`

**迁移文件**:
- `migrateFennecToOpus.ts` — 模型迁移
- `migrateSonnet1mToSonnet45.ts` — 模型迁移
- `migrateBypassPermissionsAcceptedToSettings.ts` — 配置迁移

**学习要点**:
- 版本升级需要自动迁移配置
- 迁移应该是幂等的
- 模型名称变化需要处理

---

### 12. Tool 抽象

**文件**: `src/Tool.ts`

**关键类型**:

```typescript
type Tool<Input extends Record<string, unknown>> = {
  name: string
  description: (input: Input, context: ToolContext) => Promise<string>
  inputSchema: ToolInputJSONSchema
  run: (input: Input, context: ToolUseContext) => Promise<ToolResult>
}

type ToolUseContext = {
  getAppState: () => AppState
  options: {
    isNonInteractiveSession: boolean
    toolPermissionContext: ToolPermissionContext
    tools: Tools
  }
}
```

**学习要点**:
- 工具应该有统一的抽象
- 上下文包含权限和状态
- 描述是动态生成的

---

## 可借鉴设计（新增）

### 1. 压缩 Hook 增强

```typescript
// ~/.openclaw/hooks/smart-compact/handler.ts

const handler = async (event) => {
  if (event.type !== 'session' || event.action !== 'compact:before') {
    return
  }

  // 类似 Claude Code 的压缩提示词设计
  const context = event.context

  // 1. 提取用户消息
  // 2. 提取关键决策
  // 3. 提取当前工作
  // 4. 生成下一步建议

  event.context.compactHint = generateCompactHint(context)
}
```

### 2. 权限拒绝追踪

```typescript
// ~/.openclaw/hooks/denial-tracker/handler.ts

const DENIAL_LIMITS = {
  maxDenials: 3,
  cooldownMs: 60000
}

const denialState = new Map<string, DenialTrackingState>()

const handler = async (event) => {
  if (event.type !== 'tool' || event.action !== 'denied') {
    return
  }

  const sessionId = event.sessionKey
  const state = denialState.get(sessionId) || createDenialTrackingState()

  recordDenial(state, event.context.toolName)

  if (shouldFallbackToPrompting(state)) {
    event.messages.push('⚠️ 多次拒绝检测，请确认操作意图')
  }
}
```

### 3. 迁移系统

```typescript
// 为 OpenClaw 创建迁移系统
// 在版本升级时自动迁移配置

const migrations = [
  { version: '2026.3.28', migrate: migrateToSafeBins },
  { version: '2026.4.1', migrate: migrateToNewAgentConfig },
]

function runMigrations(currentVersion: string, config: object) {
  for (const { version, migrate } of migrations) {
    if (shouldRun(config.lastMigratedVersion, version)) {
      config = migrate(config)
    }
  }
  return config
}
```

---

## 学习优先级（更新）

| 优先级 | 模块 | 价值 | 难度 | 建议 |
|-------|------|------|------|------|
| 1 | Bash 安全 | 高 | 中 | 已配置 |
| 2 | Compact 系统 | 高 | 中 | **值得深入** |
| 3 | Permission 系统 | 高 | 高 | 学习设计 |
| 4 | Token Budget | 中 | 低 | 已实现 |
| 5 | MCP 服务 | 中 | 高 | 了解即可 |
| 6 | State 管理 | 中 | 中 | 学习设计 |
| 7 | Migrations | 中 | 低 | **值得实现** |
| 8 | Tool 抽象 | 高 | 中 | 学习设计 |

---

## 源码宝藏清单

| 文件 | 行数 | 价值 | 状态 |
|------|------|------|------|
| `BashTool/bashSecurity.ts` | 1700+ | ⭐⭐⭐⭐⭐ | 已学习 |
| `coordinator/coordinatorMode.ts` | 300+ | ⭐⭐⭐⭐ | 已学习 |
| `services/compact/compact.ts` | 1700+ | ⭐⭐⭐⭐⭐ | **待深入** |
| `utils/permissions/permissions.ts` | 1400+ | ⭐⭐⭐⭐ | **待深入** |
| `QueryEngine.ts` | 1000+ | ⭐⭐⭐⭐ | 待学习 |
| `Tool.ts` | 500+ | ⭐⭐⭐ | 待学习 |
| `AgentTool/prompt.ts` | 300+ | ⭐⭐⭐⭐ | 已学习 |
| `services/compact/prompt.ts` | 300+ | ⭐⭐⭐⭐ | **待深入** |

---

*Created: 2026-03-31*
*Status: 深度学习中（未完成）*
