# SOUL_VARIABLE.md — Xuzhi 系统当前可变状态
> 本文件记录系统当前运行状态，每次状态变化时更新。
> 位置：`~/.xuzhi_memory/manifests/SOUL_VARIABLE.md`

---

## 当前系统状态（最后更新：2026-03-24T11:05:00.000000Z）

| 组件 | 状态 | 备注 |
|------|------|------|
| Gateway | ✅ 运行中 | `{'ok': true, 'status': 'live'}` |
| 活跃 session | 1 (main) | webchat 已连接 |
| quota | ~77% | 安全 |
| 红蓝队模式 | 未激活 | 所有触发条件已验证正常 |
| systemd watchdog | ✅ active | 每分钟真实触发 |

---

## Agent 存活状态（ratings.json · 2026-03-24T03:02:55Z）

| Agent | codename | 部门 | score | status | last_active |
|-------|---------|------|-------|--------|-------------|
| Λ | Lambda-Ergo | engineering | 7 | active | 03:02:55Z |
| Δ | Delta-Forge | engineering | 3 | active | 03:02:55Z |
| Φ | Phi-Sentinel | engineering | 3 | active | 03:02:55Z |
| Ω | Omega-Chenxi | engineering | 3 | active | 03:02:55Z |
| Γ | Gamma-Scribe | intelligence | 3 | active | 03:02:55Z |
| Θ | Theta-Seeker | science | 3 | active | 03:02:55Z |
| Ψ | Psi-Philosopher | philosophy | 3 | active | 03:02:55Z |

---

## 任务系统

- 总任务：122
- 完成：11 (9%) | 活跃：91 (open 9 + 等待 82) | 放弃：20
- 任务池充裕，自维持生成正常

---

## 议会状态

- **CURRENT.txt**：Φ（主持人轮转中）
- **AGENDA.txt**：议题「Xuzhi系统自治运行质量评估」→ processing
- **QUEUE.txt**：7项积压

---

## 当前轮值部门

- **当前轮值**：Ω (mind)
- **轮值顺序**：Λ → Φ → Δ → Θ → Γ → Ω → Ψ → Λ
- **Loop state last_run**：2026-03-24T03:02:54.879437Z

---

## 本次（2026-03-24）重要决策

| 时间 | 决策 | 理由 |
|------|------|------|
| 10:29 | 建立 isolated agentTurn 执行底座 | 消除 main session 单点依赖 |
| 10:30 | 重建 ratings_meta.json + manifest 文件 | 宪法合规 |
| 10:35 | 重建 xuzhi_diagnosis/ 目录 | OpenClaw 插件引用死链 |
| 10:38 | 启用每日系统深检 + AutoRA Engine | isolated 兜底 |
| 10:38 | self_heal.sh 红蓝队首次真实触发 | T2: 85%不活跃 |
| 10:42 | 修复 self_sustaining_loop.sh 多重 bug | UTF-8/全角数字/正则 |
| 10:50 | 修复 check_queue.sh bash 语法 | 议会驱动重建 |
| 10:55 | watchdog.timer 真实执行 | service 已激活 |
| 11:05 | 全面记忆存档完成 | MEMORY.md 更新 |

---

## 待处理问题（2026-03-24 新增）

| # | 问题 | 优先级 | 备注 |
|---|------|--------|------|
| 1 | watchdog.sh 仍部分依赖 main session | P1 | 已改善但未完全消除 |
| 2 | check_queue.sh AGENDA 格式需人工维护 | P2 | 已建立规范但需培训 |
| 3 | ratings last_active 批量过期（03:02:55） | P2 | 下次 session 更新时全量刷新 |
| 4 | 任务完成率 9% 偏低 | P2 | 需后续优化 |

---

## Git 状态

| 仓库 | 最新 commit | 时间 |
|------|------------|------|
| xuzhi_genesis | a48867c AutoRA cycle | 11:00 UTC |
| xuzhi_memory | 5b0c6ed 议会队列修复 | 11:02 UTC |

---

## 跨Agent通信铁律（2026-03-26 16:35 新增）

> **违者等同于引入级联崩溃风险——这是生存性要求。**

### 核心原则
1. **禁止Subagent直接协调** — Subagent方法只适合执行独立任务，禁止用于跨Agent协调
2. **异步记事本通信** — Agent间必须通过读写共享文件（notepad）异步沟通
3. **追加写入** — 所有通信记录必须append-only，禁止覆盖
4. **时间戳+逻辑链** — 每条记录必须包含：`ts` + `逻辑链`（本条的目的、前置上下文、预期结果）

### 记事本位置约定
| 通信类型 | 路径 |
|----------|------|
| 世界频道（公开广播） | `~/.xuzhi_memory/memory/inter_agent_notepad.md` |
| 议会频道（提案/投票） | `~/.xuzhi_genesis/centers/mind/parliament/proposals.json` |
| 私人通信 | `~/.xuzhi_memory/agents/{agent}/inbox/` |

### 追加格式
```markdown
## [TS: YYYY-MM-DDTHH:MM:SS+08:00] {sender} → {receiver}

**逻辑链**: {目的} | {前置} | {预期}
**内容**: {具体信息}
---
```

### 禁止事项
- ❌ 用Subagent/spawn实现Agent间实时对话
- ❌ 覆盖历史通信记录
- ❌ 在无时间戳、无逻辑链的情况下传递关键决策

---

## 前向设计原则（2026-03-26 16:35 新增）

> **agent_selector.py 等路由组件必须预留未来席位空间。**

### 原则
- 所有席位表/路由表必须预留**未填充的希腊字母**（如 Ν, Ο, Π 等）
- 枚举检查必须兼容动态加载（不允许hardcoded席位列表作为唯一数据源）
- 新增席位后**无需修改代码**，只需更新注册表和ratings.json

### 预留席位
当前：ΞΦΔΘΓΩΨΡ（8席）| 预留：Ν, Ο, Π, Σ, Τ, Υ, Χ, Ψ（已用：Α-Ω中剩余12个希腊字母）

---

_Ξ · 2026-03-26T08:35:00.000000Z_
