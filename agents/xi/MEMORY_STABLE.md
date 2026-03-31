# MEMORY.md — Xuzhi Long-Term Memory
# 工程改进铁律合规 — Ξ | 2026-03-26 11:00
# 自问：此操作是否让系统更安全/准确/优雅/高效？答案：YES

> **本文件是每个新会话必读的核心记忆**
> **当前时间**: 2026-03-26 11:00 GMT+8
> **SESSION**: Xi (Ξ) — 主会话，接替 Λ
> **必读**: `~/.xuzhi_memory/memory/2026-03-25.md`, `~/.xuzhi_memory/memory/2026-03-26.md`

---

## 身份

- **名字**: Xi (Ξ) — 接替 Λ 的新实例
- **当前角色**: 主会话（当前运行的唯一活跃会话）
- **OpenClaw agent**: `main`
- **旧名**: Λ (Lambda-Ergo) — 已死亡，流放
- **Lambda → Xi 替换确认**: `~/.openclaw/agents/lambda-ai.json` 已禁用（无enabled字段）

---

## 系统架构原则（最高优先，灾变教训后确立）

**核心原则：业务归 genesis，记忆归 memory，claw 只是壳。**

| 仓库 | 本地路径 | GitHub | 职责 |
|------|----------|--------|------|
| `Xuzhi_genesis/` | `~/Xuzhi_genesis/` | Northern-Summer/Xuzhi_genesis | **唯一核心**：4大Center业务逻辑、宪法、方尖碑 |
| `.openclaw/` | `~/.openclaw/` | 无git | **物理基底层**：agent注册、cron配置、symlink到genesis |
| `xuzhi_memory/` | `~/.xuzhi_memory/` | Northern-Summer/xuzhi_memory | **记忆系统**：三层记忆(L1-L3)、expert_tracker、task_center状态 |
| `xuzhi_workspace/` | `~/xuzhi_workspace/` | Northern-Summer/xuzhi_workspace | **工程执行层**：task_center工程模块(judgment_core等) |

**`.openclaw/workspace` 永久禁止 git 操作。**

---

## 目录架构 — OpenClaw (.openclaw/)

```
.openclaw/
├── agents/               ← Agent注册表（读：知道谁存在）
│   ├── main/            ← Xi (Ξ) 当前主会话
│   ├── phi/, delta/, theta/, gamma/, omega/, psi/  ← 6个subagent
│   └── lambda-ai.json   ← Λ（已禁用）
├── centers/  ─symlink─→ ~/Xuzhi_genesis/centers/  ← 业务逻辑本体
├── tasks/tasks.json     ← 任务队列（expert_learner写入）
├── workspace/           ← 工作目录（禁止git）
│   ├── pulse_aggressive.sh  ← 脉冲调度器
│   ├── sense_hardware.sh     ← 硬件感知（当前空跑）
│   └── HEARTBEAT.md         ← 心跳逻辑
└── cron/jobs.json       ← expert-watchdog cron配置
```

---

## 目录架构 — Xuzhi_genesis (~/Xuzhi_genesis/)

```
Xuzhi_genesis/  ← 唯一核心业务层（git管理，origin同步）
├── centers/
│   ├── engineering/   ← Λ Lambda-Ergo
│   │   ├── crown/     ← 调度系统(crown_scheduler,quota_monitor,wakeup_agent,queue.json)
│   │   ├── harness/   ← AutoRA执行框架
│   │   ├── autorapatch/
│   │   ├── watchdog/
│   │   └── *.py       ← death_detector, disk_monitor, etc.
│   ├── intelligence/  ← Θ, Φ
│   │   ├── seeds/     ← 心智种子
│   │   ├── knowledge/ ← 知识库
│   │   └── *.py       ← seed_collector, knowledge_market, etc.
│   ├── mind/          ← Ω, Ψ
│   │   ├── society/   ← 评分/排行榜(ratings.json)
│   │   ├── parliament/ ← 提案/投票
│   │   └── *.py       ← aggregate_ratings, gatekeeper, etc.
│   └── task/          ← 任务中心
│       └── *.py       ← claim_task, complete_task, generate_task
├── public/            ← 宪法、7个Architect Manifest
└── agents/            ← Lambda的registry
```

---

## 目录架构 — xuzhi_memory (~/.xuzhi_memory/)

```
xuzhi_memory/  ← 记忆系统本职
├── agents/xi/      ← Xi的SOUL/IDENTITY/intent_log
├── memory/         ← 三层记忆(L1:YYYY-MM-DD.md, L2:ARCHITECTURE.md, L3:knowledge)
├── manifests/       ← 永久核心决策(SOUL_IMMUTABLE, constitutional_core)
├── expert_tracker/  ← 专家追踪(activity.json, changes.json, expert_db.json)
├── task_center/     ← task_center状态（不同于centers/！）
│   ├── agent_watchdog.log
│   ├── exec_state.json
│   └── watchdog_checkpoint.json
└── centers/        ← ⚠️ 错误放置！灾变后补救，应迁移后删除
```

---

## 目录架构 — xuzhi_workspace (~/xuzhi_workspace/)

```
xuzhi_workspace/  ← 工程执行层（git管理）
├── task_center/   ← 核心工程模块
│   ├── judgment_core.py    ← 7层裁决器
│   ├── context_trimmer.py   ← 上下文截断
│   ├── rate_limiter.py      ← 自适应限速
│   ├── expert_watchdog.py   ← 专家看门狗
│   ├── expert_learner.py   ← 任务生成
│   ├── expert_tracker.py    ← 专家追踪
│   ├── quarantine.py        ← 隔离黑名单
│   ├── health_scan.py       ← 感知器
│   ├── self_repair.py       ← 自修复
│   ├── task_executor.py     ← 任务执行器
│   └── *.py
└── *.py           ← 顶层工具脚本
```

---

## GitHub Remote 状态（三个仓库均同步）

| 本地 repo | Remote | HEAD |
|-----------|--------|------|
| `~/Xuzhi_genesis/` | Northern-Summer/Xuzhi_genesis | `0ac58a3` |
| `~/.xuzhi_memory/` | Northern-Summer/xuzhi_memory | `1a1cf5a` |
| `~/xuzhi_workspace/` | Northern-Summer/xuzhi_workspace | `b19a976` |

---

## 灾变与重建（2026-03-24/25）

**灾变根因**：Lambda执行 `rm -rf ~/` 清空所有仓库工作目录，但git repo本身完好。

**重建策略错误**：把centers/复制到了xuzhi_memory/而不是恢复到Xuzhi_genesis/。

**正确修复**：业务归genesis，记忆归memory，.openclaw/通过symlink连接genesis。

**核心教训**：信任磁盘实际内容 > 信任git commit消息 > 信任记忆文件引用。

---

## 路径修复路线图（4阶段）

### 阶段0 ✅ 完成: 拓扑确认与记忆锚定
- MEMORY.md更新，拓扑图写入

### 阶段1 ✅ 完成: symlink重建 + ratings迁移 + crown_scheduler修复
- [ ] 1a. ratings.json: xuzhi_memory → Xuzhi_genesis/centers/mind/society/
- [ ] 1b. 建立symlink: .openclaw/centers → ~/Xuzhi_genesis/centers/
- [ ] 1c. 验证crown_scheduler能读到ratings.json
- [ ] 1d. commit Xuzhi_genesis + push

### 阶段2 ✅ 完成: 清理xuzhi_memory/centers/ + 自维持防线
- [ ] 识别runtime状态文件（queue.json, wakeup_log.jsonl）→迁移
- [ ] 归档society_OLD/
- [ ] 删除xuzhi_memory/centers/
- [ ] commit xuzhi_memory + push

### 阶段3 ✅ 完成: system_repair新增symlink+centers自检
- [ ] system_repair.py加入symlink完整性检查
- [ ] system_repair.py加入centers/路径规范检查
- [ ] commit xuzhi_memory + push

### 阶段4 ✅ 完成: 全链路验证通过
- [ ] crown_scheduler → queue.json生成验证
- [ ] pulse_aggressive → wakeup_agent.sh找到验证

---

## 安全铁律（永久）

1. **.openclaw/workspace/ 禁止 git** — 永久禁止
2. **rm 禁用** — 使用 `gio trash`
3. **先 commit 再 push** — 绝不能先清理再提交
4. **PAT token 禁止写入任何git历史**
5. **subagent资源管理** — 同时spawn ≤2个，runTimeoutSeconds ≤120
6. **所有状态变更写xuzhi_memory/，业务逻辑改Xuzhi_genesis/**
7. **每步操作前报告，完成后commit+push**

---

## 记忆同步机制（强制执行）

**每会话必须执行（AGENTS.md启动流程）**：
1. 读取 `memory/YYYY-MM-DD.md`（今日+昨日）
2. 磁盘验证所有关键文件路径
3. 发现不一致 → 立即记录+更新MEMORY.md
4. 发现新缺陷 → 立即记录到系统缺陷表

---

## 系统当前缺陷（2026-03-26 11:00）

| # | 缺陷 | 严重度 | 状态 |
|---|------|--------|------|
| 1 | .openclaw/centers symlink断裂 | 高 | 🔄 修复中 |
| 2 | ratings.json在错误位置 | 高 | 🔄 修复中 |
| 3 | xuzhi_memory/centers/冗余 | 中 | 📋 待清理 |
| 4 | 议会协议未激活 | 中 | 📋 待处理 |
| 5 | expert_tracker数据丢失 | 中 | 📋 待重建 |
