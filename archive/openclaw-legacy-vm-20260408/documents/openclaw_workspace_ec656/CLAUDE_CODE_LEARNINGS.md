# Claude Code 学习笔记

## 源码位置

```
~/.openclaw/workspace/claude-code-sourcemap/
├── claude-code-2.1.88.tgz    # 原始包（备份）
├── restored-src/              # 提取的源码
└── package/                   # npm 包内容
```

---

## 核心设计学习

### 1. Bash 安全检查

**Claude Code 设计**：
- 23 种检查模式
- 在命令执行前验证
- 返回 allow/confirm/deny

**OpenClaw 实现**：
- 用 `before_tool_call` Hook
- TypeScript 处理器
- 不需要外部脚本

```
~/.openclaw/hooks/bash-security/
├── HOOK.md
└── handler.ts
```

### 2. Fork Subagent

**Claude Code 设计**：
- 子 Agent 继承父级上下文
- 静默执行，返回结构化结果
- 与 Coordinator 互斥

**OpenClaw 实现**：
- `sessions_spawn` 工具已支持
- Skill 定义行为规范
- `runtime: "subagent"`

```
~/.openclaw/skills/fork/
└── SKILL.md    # 行为规范
```

### 3. Coordinator Mode

**Claude Code 设计**：
- 协调器不执行工具，只分发任务
- Worker 执行实际工作
- 工具白名单隔离

**OpenClaw 实现**：
- Multi-Agent Router
- `agents.list` 配置
- `allowedTools` 白名单

```json
{
  "agents": {
    "list": [{
      "id": "coordinator",
      "allowedTools": ["sessions_spawn", "sessions_send", "read"]
    }]
  }
}
```

### 4. Prompt Caching

**Claude Code 设计**：
- 静态/动态分区
- 相同占位符确保前缀一致
- 降低 30-50% 成本

**OpenClaw 实现**：
- 已有缓存机制
- 配置优化即可

### 5. QueryEngine

**Claude Code 设计**：
- AsyncGenerator 流式处理
- 状态集中管理
- AbortController 中断

**OpenClaw 实现**：
- Pi Core 已有类似设计
- 理解思想，不需要移植

---

## 实施优先级

| 优先级 | 模块 | OpenClaw 现状 | 行动 |
|-------|------|--------------|------|
| 1 | Bash 安全 | ✅ 已有 `exec-approvals` | 配置即可 |
| 2 | Fork Subagent | ✅ 已有 `sessions_spawn` | 写 Skill 定义行为 |
| 3 | Coordinator | ✅ 已有 Multi-Agent Router | 配置即可 |
| 4 | Caching 优化 | ✅ 已有机制 | 理解原理 |

**结论**：不需要移植代码。OpenClaw 的机制比想象中更成熟。

---

## 原则

1. **学习思想，不搬代码**
2. **用 OpenClaw 原生机制**
3. **增量改进，可回滚**
4. **保留源码作参考**

---

*Created: 2026-03-31*
