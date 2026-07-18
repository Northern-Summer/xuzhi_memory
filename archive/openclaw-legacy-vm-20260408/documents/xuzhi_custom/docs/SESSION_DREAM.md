# Session Dream — 智能 Session 整合机制

## 设计理念

借鉴 Claude Code 的 **autoDream** 设计，采用**四阶段智能整合**流程，而非暴力删除。

---

## 核心机制

### 三重门控

```
时间门控 → 会话门控 → 锁门控
   ↓           ↓          ↓
>= 24h      >= 30      无其他进程
```

**目的**：避免频繁执行，确保只在真正需要时整合。

### 四阶段流程

```
┌─────────────────────────────────────────────────────────────────┐
│                    Session Dream 四阶段                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 1 — Orient（定位）                                        │
│  ─────────────────────                                          │
│  扫描所有 agent 的 sessions                                      │
│  解析类型、状态、时间、token 使用量                               │
│                                                                 │
│  Phase 2 — Analyze（分析）                                       │
│  ─────────────────────                                          │
│  智能判断哪些 session 可以归档：                                  │
│                                                                 │
│  保留条件（满足任一）：                                           │
│  ✅ 用户创建的 session（保留 7 天）                               │
│  ✅ 包含重要决策的 session                                       │
│  ✅ 大 session（> 50k tokens）                                   │
│  ✅ 最近活跃的 session（< 3 天）                                 │
│  ✅ 活跃状态的 session                                          │
│                                                                 │
│  归档条件（不满足任何保留条件）：                                  │
│  ❌ cron/subagent 创建                                          │
│  ❌ 超过 3 天未活跃                                              │
│  ❌ 已完成/中止状态                                              │
│  ❌ token 使用量低                                              │
│                                                                 │
│  Phase 3 — Archive（归档）                                       │
│  ─────────────────────                                          │
│  压缩归档，保留摘要：                                             │
│  - 生成 session 摘要（JSON 格式）                                │
│  - 原文件标记为 .archived                                       │
│  - 不直接删除，可恢复                                            │
│                                                                 │
│  Phase 4 — Index（索引）                                         │
│  ─────────────────────                                          │
│  不修改 sessions.json（让 OpenClaw 自己管理）                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 使用方式

### 命令行

```bash
# 显示统计
python3 ~/.openclaw/workspace/session_dream.py stats

# 执行整合（遵循门控）
python3 ~/.openclaw/workspace/session_dream.py run

# 强制执行（跳过门控）
python3 ~/.openclaw/workspace/session_dream.py force
```

### 定时任务

每天 3:00 自动执行。

---

## 当前状态

```
总计: 90 sessions

按类型:
  user: 22      ← 保留优先级最高
  cron: 46      ← 归档优先级最高
  subagent: 21  ← 归档优先级高
  heartbeat: 1  ← 归档优先级高

按状态:
  completed: 62  ← 可归档
  idle: 24       ← 可归档
  aborted: 4     ← 可归档

按年龄:
  <1d: 29   ← 保留
  1-3d: 15  ← 可归档
  3-7d: 46  ← 归档
  >7d: 0

分析结果:
  保留: 53 sessions
  归档: 37 sessions
```

---

## 与暴力清理的对比

| 特性 | 暴力清理 | Session Dream |
|------|----------|---------------|
| 判断标准 | 时间 alone | 多维度智能判断 |
| 用户 session | 无差别 | 保留 7 天 |
| 重要决策 | 不检查 | 检查并保留 |
| 大 session | 不检查 | 检查并保留 |
| 删除方式 | 直接删除 | 归档 + 摘要 |
| 可恢复性 | ❌ | ✅ |
| 与 OpenClaw 融合 | ❌ | ✅ |

---

## 配置

```python
DEFAULT_CONFIG = {
    "min_hours": 24,           # 时间门控阈值
    "min_sessions": 30,        # 会话门控阈值
    "archive_days": 3,         # 归档阈值
    "keep_user_sessions": 7,   # 用户 session 保留天数
    "keep_large_sessions": True,
    "large_session_threshold": 50000,  # 大 session 阈值
}
```

---

## 文件位置

```
~/.openclaw/workspace/session_dream.py      ← 主脚本
~/.openclaw/.session-dream.lock             ← 整合锁
~/.openclaw/.session-dream-state.json       ← 状态文件
~/.openclaw/sessions-archive/               ← 归档目录
```

---

## 灵感来源

Claude Code 的 **autoDream** 机制：

- 三重门控：时间 + 会话 + 锁
- 四阶段流程：定位 → 分析 → 整合 → 索引
- 只读权限，安全操作
- 智能判断，不穷举

---

*Created: 2026-04-01*
*Inspired by: Claude Code autoDream*
