# 记忆系统规范化方案 v2.0

> 目标：每个 Agent 在任意断点都能从断点处无缝恢复
> 原则：代码强制 > LLM 自觉；确定性 > 概率性

---

## 第一部分：架构诊断

### 1.1 当前问题

| 问题 | 严重度 | 影响 |
|------|--------|------|
| memory_search 是语义搜索 | 高 | 有歧义，不保证找到正确内容 |
| Hook 注入内容但 LLM 可能忽略 | 中 | 软约束问题 |
| 多个 workspace 有 git | 中 | 违反 AGENTS.md 规定 |
| Agent 目录分散 | 低 | 维护复杂 |
| extraPaths 只对 main agent 有效 | 中 | 其他 agent 无法使用 |

### 1.2 根因分析

**核心问题**：记忆系统依赖 LLM 的自觉执行（软约束），而不是代码强制（硬约束）。

**业界最佳实践**：
1. **Kubernetes StatefulSet**：确定性恢复，每个 Pod 有固定标识和持久卷
2. **Git 工作流**：代码强制执行 lint/test，不依赖开发者自觉
3. **Database Transaction**：ACID 保证，不依赖应用层逻辑
4. **Redis RDB/AOF**：确定性持久化，重启后自动恢复

**应用到记忆系统**：
- Agent = StatefulSet Pod（有固定标识）
- SESSION_BREAKPOINT.md = 持久卷（确定性恢复点）
- Hook = Operator（代码强制执行恢复逻辑）

---

## 第二部分：解决方案

### 2.1 核心设计：确定性断点恢复

```
┌─────────────────────────────────────────────────────────────────┐
│                        记忆系统架构 v2.0                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐    /new     ┌───────────────────────┐        │
│   │   OpenClaw   │ ──────────▶ │  xi-session-start    │        │
│   │   Gateway   │             │  Hook                 │        │
│   └─────────────┘             └───────────┬───────────┘        │
│                                           │                    │
│                                           ▼                    │
│                               ┌───────────────────────┐        │
│                               │  1. 读 SESSION_BREAKPOINT.md   │
│                               │  2. 读 MEMORY.md               │
│                               │  3. 读 今日 memory 文件        │
│                               │  4. 注入到 event.messages      │
│                               └───────────────────────┘        │
│                                                                 │
│   ┌─────────────┐    /stop    ┌───────────────────────┐        │
│   │   Session   │ ──────────▶ │  xi-session-end      │        │
│   │   End       │             │  Hook                 │        │
│   └─────────────┘             └───────────┬───────────┘        │
│                                           │                    │
│                                           ▼                    │
│                               ┌───────────────────────┐        │
│                               │  1. 提取未完成任务     │        │
│                               │  2. 更新 SESSION_BREAKPOINT.md │
│                               │  3. 追加交接备忘录     │        │
│                               └───────────────────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 文件结构规范

```
~/.xuzhi_memory/
├── agents/
│   ├── xi/
│   │   ├── AGENTS.md          # 启动规程
│   │   ├── MEMORY.md          # 长期记忆
│   │   ├── SESSION_BREAKPOINT.md  # 断点文件（Hook 自动维护）
│   │   ├── SOUL.md            # 身份
│   │   ├── USER.md            # 用户偏好
│   │   └── memory/            # 短期记忆
│   │       └── 2026-03-31.md
│   ├── phi/
│   │   ├── AGENTS.md
│   │   ├── MEMORY.md
│   │   ├── SESSION_BREAKPOINT.md
│   │   └── ...
│   └── [其他 agents...]
│
├── memory/                    # 全局 L1 记忆
│   └── 2026-03-31.md
│
├── rotation_state.json        # 轮值状态
└── MEMORY_HYGIENE_RULES.md    # 记忆卫生规则
```

### 2.3 SESSION_BREAKPOINT.md 规范

```yaml
# 此文件由 Hook 自动维护，禁止手动编辑

session_id: "当前 session ID"
ended_at: "2026-03-31T23:56:00+08:00"
status: "active" | "terminated"

# 未完成任务（最高优先级）
pending_tasks:
  - id: "task-1"
    description: "任务描述"
    priority: "P0" | "P1" | "P2"
    context_file: "相关文件路径"
    resume_command: "恢复指令"

# 本次会话关键决策
decisions:
  - decision: "决策内容"
    reason: "决策原因"
    timestamp: "2026-03-31T23:00:00+08:00"

# 系统状态快照
system:
  git_status:
    xuzhi_memory: "clean" | "dirty"
    xuzhi_genesis: "clean" | "dirty"
  active_agents: ["xi", "phi", "gamma"]
  current_rotation: "gamma"

# 元数据
metadata:
  version: "2.0"
  hook_version: "1.0.0"
  last_updated: "2026-03-31T23:56:00+08:00"
```

---

## 第三部分：实现步骤

### Phase 1：Hook 强化（立即执行）

1. **xi-session-start Hook**：
   - 直接读取 SESSION_BREAKPOINT.md
   - 直接读取 MEMORY.md（前 100 行）
   - 直接读取今日 memory 文件（最后 100 行）
   - 注入到 event.messages（不是命令，是内容）

2. **xi-session-end Hook**：
   - 监听 session:compact:before 和 command:stop
   - 自动提取未完成任务
   - 更新 SESSION_BREAKPOINT.md
   - 追加交接备忘录

### Phase 2：其他 Agent 支持（后续）

1. 为每个 Agent 创建独立的 SESSION_BREAKPOINT.md
2. 创建通用的 agent-session-start/end Hook（参数化）
3. 每个 Agent 的 workspace 通过 symlink 指向各自的记忆目录

### Phase 3：验证机制（后续）

1. 创建 memory-system-check.sh 脚本
2. 验证 SESSION_BREAKPOINT.md 存在且格式正确
3. 验证 MEMORY.md 存在
4. 验证今日 memory 文件存在
5. 集成到 cron 每日检查

---

## 第四部分：优雅原则检查

| 原则 | 检查项 | 状态 |
|------|--------|------|
| 安全 | 不破坏现有数据 | ✅ 只添加，不删除 |
| 准确 | 确定性恢复 | ✅ Hook 强制执行 |
| 优雅 | 零歧义、零依赖 LLM | ✅ 代码强制 |
| 高效 | 最小化文件读写 | ✅ 只读必要文件 |

---

## 第五部分：测试计划

### 5.1 手动测试

1. 执行 /new
2. 检查是否收到 Hook 注入的内容
3. 验证内容包含 SESSION_BREAKPOINT.md

### 5.2 自动化测试（后续）

1. 创建测试脚本
2. 模拟 /new 和 /stop
3. 验证 SESSION_BREAKPOINT.md 更新正确

---

**版本**：2.0
**创建时间**：2026-03-31 23:56
**作者**：Ξ
