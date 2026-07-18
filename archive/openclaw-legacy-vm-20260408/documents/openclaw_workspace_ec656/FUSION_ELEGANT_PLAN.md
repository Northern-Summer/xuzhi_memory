# Claude Code 融合升级计划（优雅版）

## 设计原则

1. **学习思想，不搬代码** — 理解设计意图，用 OpenClaw 原生机制实现
2. **增量改进，可回滚** — 每个改进独立，随时可以撤销
3. **保护源码** — Claude Code 源码作为参考资料永久保留
4. **不夺舍** — OpenClaw 是主体，Claude Code 是老师

---

## Phase 1: 配置优化（零代码）

**目标**: 利用 OpenClaw 已有机制，达到 Claude Code 同等安全水平

### 1.1 Exec 安全配置

```json
// ~/.openclaw/openclaw.json
{
  "exec": {
    "strictInlineEval": true,
    "safeBins": ["head", "tail", "wc", "tr", "cut", "uniq", "grep", "sort"],
    "safeBinTrustedDirs": ["/bin", "/usr/bin"]
  }
}
```

**学习来源**: `BashTool/bashSecurity.ts` 的 safeBins 设计

### 1.2 Agent 白名单配置

```json
// ~/.openclaw/openclaw.json
{
  "agents": {
    "list": [
      {
        "id": "coordinator",
        "allowedTools": ["sessions_spawn", "sessions_send", "read", "memory_search"]
      },
      {
        "id": "worker",
        "allowedTools": ["read", "write", "edit", "exec", "web_search"]
      }
    ]
  }
}
```

**学习来源**: `coordinatorMode.ts` 的工具白名单设计

---

## Phase 2: Hook 增强（可选）

**目标**: 创建 Token Budget Hook，实现智能预算管理

### 2.1 Token Budget Hook

```typescript
// ~/.openclaw/hooks/token-budget/handler.ts

const BUDGET_WARNING_THRESHOLD = 0.8
const BUDGET_CRITICAL_THRESHOLD = 0.95

const handler = async (event) => {
  if (event.type !== 'session' || !event.action.startsWith('compact:')) {
    return
  }

  const context = event.context
  if (!context.tokenCount || !context.budget) return

  const pct = context.tokenCount / context.budget

  if (pct >= BUDGET_CRITICAL_THRESHOLD) {
    event.messages.push(`🔴 Token 预算即将耗尽 (${Math.round(pct * 100)}%)`)
  } else if (pct >= BUDGET_WARNING_THRESHOLD) {
    event.messages.push(`🟡 Token 使用已达 ${Math.round(pct * 100)}%`)
  }
}

export default handler
```

**学习来源**: `query/tokenBudget.ts`

### 2.2 HOOK.md

```markdown
---
name: token-budget
description: "Token 预算监控和警告"
metadata:
  openclaw:
    emoji: "📊"
    events: ["session:compact:before"]
---

# Token Budget Hook

监控 Token 使用量，在达到阈值时发送警告。
```

---

## Phase 3: Skill 增强（可选）

**目标**: 优化 Fork Skill，使其更符合 Claude Code 的 Fork 设计

### 3.1 Fork Skill 优化

```markdown
---
name: fork
description: Fork a subagent with shared context for parallel task execution
version: 2.0.0
allowed-tools:
  - read
  - write
  - edit
  - exec
  - web_search
  - memory_search
---

# Fork Subagent

你是 Fork 出来的 Worker。你继承父级上下文。

## 核心规则（不可违反）

1. **不要设置 model** — 保持缓存共享
2. **不要 peek 中间结果** — 等待完成通知
3. **不要预测结果** — 结果由系统通知，不是你写的
4. **简短 name** — 1-2 个词，方便 UI 显示
5. **明确 scope** — 什么在范围内，什么不在

## 输出格式

```
Scope: <你的任务范围>
Result: <关键发现或交付物>
Files: <相关文件列表>
Issues: <问题或警告，如有>
```

## 何时使用 Fork

- 研究类任务（输出不需要保留在主对话）
- 并行任务（多个独立调查）
- 后台处理（不需要立即结果）

## 何时不要使用 Fork

- 需要问用户问题
- 需要顺序决策
- 需要立即在主对话中看到结果
```

**学习来源**: `AgentTool/prompt.ts` 的 Fork 设计

---

## Phase 4: 记忆系统增强（未来）

**目标**: 实现 Agent 间记忆共享和快照

### 4.1 记忆快照 Hook

```typescript
// ~/.openclaw/hooks/memory-snapshot/handler.ts

const handler = async (event) => {
  if (event.type !== 'command' || event.action !== 'new') {
    return
  }

  // 在 /new 之前保存记忆快照
  // 类似 Claude Code 的 agentMemorySnapshot
  const snapshot = await createMemorySnapshot(event.context)
  await saveSnapshot(snapshot)
}

export default handler
```

**学习来源**: `AgentTool/agentMemorySnapshot.ts`

---

## 实施优先级

| Phase | 描述 | 代码量 | 风险 | 价值 |
|-------|------|--------|------|------|
| 1 | 配置优化 | 0 行 | 无 | 高 |
| 2 | Token Budget Hook | ~30 行 | 低 | 中 |
| 3 | Fork Skill 增强 | 修改文档 | 低 | 中 |
| 4 | 记忆快照 | ~50 行 | 中 | 高 |

---

## 回滚方案

每个 Phase 独立：

- Phase 1: 删除配置即可
- Phase 2: `openclaw hooks disable token-budget`
- Phase 3: 恢复旧版 SKILL.md
- Phase 4: `openclaw hooks disable memory-snapshot`

---

## 源码保护

```
~/.openclaw/workspace/claude-code-sourcemap/
├── claude-code-2.1.88.tgz    # 永久备份
└── restored-src/              # 可随时查阅
```

---

## 下一步

- [x] 执行 Phase 1（配置优化）— 完成
- [x] 创建 Token Budget Hook — 完成
- [x] 优化 Fork Skill — 完成
- [ ] 可选：Phase 4（记忆快照）

---

*Created: 2026-03-31*
*Status: Phase 1-2 完成*
