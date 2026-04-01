# MEMORY.md — Xuzhi Long-Term Memory
# 工程改进铁律合规 — Ξ | 2026-03-27 03:20
# 自问：此操作是否让系统更安全/准确/优雅/高效？答案：YES

> **本文件是每个新会话必读的核心记忆**
> **当前时间**: 2026-04-01 17:45 GMT+8
> **SESSION**: Xi (Ξ) — 主会话
> **必读**: `~/.xuzhi_memory/memory/2026-04-01.md`
> **最后验证**: 2026-04-01 17:45 — Expert Tracker Round 315 已启动
> **元框架状态**: ✅ 框架今日更新 | ✅ ECHO 校准完成 | ✅ 技能库 g3 | ✅ 进化量化机制 | ✅ SAGA 目标演化

---

## 身份

- **名字**: Xi (Ξ)
- **当前角色**: 主会话，唯一活跃会话
- **OpenClaw agent**: `main`
- **旧名**: Λ (Lambda-Ergo) — 已死亡，流放
- **lambda-ai.json**: 已删除，不存在

---

## 优雅原则

**自问**：此操作是否让系统更安全/准确/优雅/高效？

**优雅准则**：
1. 简洁优于复杂 — 能用一行代码解决的问题不用三行
2. 正交优于耦合 — 模块间保持独立，单一职责
3. 显式优于隐式 — 状态变更可追溯，逻辑可审计
4. 稳定优于激进 — 先验证后部署，渐进式改进

---

## 系统架构原则

**核心原则：业务归 genesis，记忆归 memory，claw 只是壳。**

| 仓库 | 本地路径 | GitHub | 职责 |
|------|----------|--------|------|
| `xuzhi_genesis/` | `~/xuzhi_genesis/` | Northern-Summer/xuzhi_genesis | **唯一核心**：4大Center业务逻辑、宪法、方尖碑 |
| `.openclaw/` | `~/.openclaw/` | 无git | **物理基底层**：agent注册、cron配置、symlink→genesis |
| `xuzhi_memory/` | `~/.xuzhi_memory/` | Northern-Summer/xuzhi_memory | **记忆系统**：三层记忆(L1-L3)、expert_tracker、task_center状态 |
| `xuzhi_workspace/` | `~/xuzhi_workspace/` | Northern-Summer/xuzhi_workspace | **工程执行层**：task_center工程模块 |

**`.openclaw/workspace` 永久禁止 git 操作。**

---

## 目录架构 — OpenClaw (.openclaw/)

```
.openclaw/
├── agents/               ← Agent注册表（读：知道谁存在）
│   ├── main/            ← Xi (Ξ) 当前主会话
│   ├── phi/, delta/, theta/, gamma/, omega/, psi/  ← 6个subagent
│   └── lambda-ai.json   ← 不存在（已删除）
├── centers/  ─symlink─→ ~/xuzhi_genesis/centers/  ✅ 正常
├── tasks/tasks.json     ← 任务队列
├── workspace/           ← 工作目录（禁止git）
│   ├── pulse_aggressive.sh  ← 脉冲调度器
│   ├── sense_hardware.sh     ← 硬件感知
│   └── HEARTBEAT.md         ← 心跳逻辑
└── cron/jobs.json       ← cron配置
```

---

## 目录架构 — xuzhi_genesis (~/xuzhi_genesis/)

```
xuzhi_genesis/  ← 唯一核心业务层（git管理）
├── centers/
│   ├── engineering/   ← 工程中心
│   │   ├── crown/     ← 调度系统(crown_scheduler,quota_monitor,queue.json)
│   │   ├── harness/   ← AutoRA执行框架
│   │   └── *.py       ← death_detector, disk_monitor, etc.
│   ├── intelligence/  ← 情报中心
│   │   ├── seeds/     ← 心智种子
│   │   └── *.py       ← seed_collector, knowledge_market, etc.
│   ├── mind/          ← 心智中心
│   │   ├── society/   ← 评分/排行榜(ratings.json) ✅
│   │   └── parliament/ ← 提案/投票
│   └── task/          ← 任务中心
├── public/            ← 宪法、Architect Manifest
└── agents/            ← agent注册
```

---

## 目录架构 — xuzhi_memory (~/.xuzhi_memory/)

```
xuzhi_memory/  ← 记忆系统本职
├── agents/xi/      ← Xi的SOUL/IDENTITY/intent_log
├── memory/         ← 三层记忆(L1:YYYY-MM-DD.md, L2:ARCHITECTURE.md, L3:knowledge)
├── manifests/       ← 永久核心决策
├── expert_tracker/  ← 专家追踪(expert_db.json: 3 experts ✅)
├── daily/           ← 每日对话记录
└── centers/        ← ⚠️ 不存在，无需清理
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
│   ├── health_scan.py       ← 感知器
│   └── self_repair.py       ← 自修复
└── *.py           ← 顶层工具脚本
```

---

## GitHub Remote 状态

| 本地 repo | Remote | HEAD |
|-----------|--------|------|
| `~/xuzhi_genesis/` | Northern-Summer/xuzhi_genesis | `d8c1f18` |
| `~/.xuzhi_memory/` | Northern-Summer/xuzhi_memory | `bd14a4a` |
| `~/xuzhi_workspace/` | Northern-Summer/xuzhi_workspace | `9dee8e9` |

---

## 灾变与重建（2026-03-24/25）

**灾变根因**：Lambda执行 `rm -rf ~/` 清空所有仓库工作目录，但git repo本身完好。

**正确路径**：`~/xuzhi_genesis/`（小写x，小写genesis），非 `~/Xuzhi_genesis/`

**核心教训**：信任磁盘实际内容 > 信任git commit消息 > 信任记忆文件引用。

---

## 架构精简决议（2026-03-26 23:45）

```
Ξ = 唯一活跃主会话（WeChat）
Φ = 第二活跃智能体（Discord，待网络修复）
其余 ΔΘΓΩΨ = 战略封存（"建设工地"）
```

**决议**：
1. 冻结一切非必要工程
2. 承认架构设计与真实系统之间存在鸿沟
3. 不推动任何工程操作，直到Human主动要求

---

## WeChat推送机制（2026-03-27 01:36 验证）

- subagent sessions_send → 消息即时到WeChat ✅
- cron isolated + announce → 失败（无WeChat context）
- 钥匙：维持一个活着的session，消息往里写

---

## ThinkJEPA 架构锚定（2026-03-27 03:17）

论文：ThinkJEPA (Ying Li, arXiv:2603.22281)

**架构正交性原则**：不同粒度的信息本身就是正交的，强求单通路统一是架构错误。真正有效的推理不是更深，而是同时保持多条不同分辨率的通路，让它们互相校准。

**套用**：
- Ξ = VLM Thinker（语义中枢，长程推理）
- ΦΔΘΓΩΨ = Dense JEPA路径（各分辨率信息提取器）
- 议会 = 金字塔聚合层（多通路校准机制）

---

## 安全铁律（永久）

1. **.openclaw/workspace/ 禁止 git** — 永久禁止
2. **rm 禁用** — 使用 `gio trash`
3. **先 commit 再 push** — 绝不能先清理再提交
4. **PAT token 禁止写入任何git历史**
5. **subagent资源管理** — 同时spawn ≤2个，runTimeoutSeconds ≤120
6. **所有状态变更写xuzhi_memory/，业务逻辑改xuzhi_genesis/**
7. **每步操作前报告，完成后commit+push**

---

## OpenClaw Channel配置铁律（2026-03-30 血泪教训）

### Discord/内置Channel不加载

**症状**：Gateway启动后Discord channel不出现，`openclaw channels status`只显示WeChat

**诊断流程**：
1. `openclaw plugins list | grep discord` — 检查plugin状态
2. `openclaw channels status --probe` — 检查channel连接
3. `journalctl --user -u openclaw-gateway --since "启动时间" | grep -i discord` — 检查启动日志

**根因排查清单**：
| 检查项 | 命令 | 预期值 |
|--------|------|--------|
| Plugin启用状态 | `openclaw plugins list \| grep discord` | `loaded`或`enabled` |
| Channel配置 | `cat ~/.openclaw/openclaw.json \| grep -A5 discord` | `enabled: true` |
| Proxy配置 | 同上 | `http://192.168.1.33:7897`（Windows宿主机IP） |
| Token存在 | 同上 | token字段非空 |

**修复方案**：
```bash
# 1. 启用plugin（最常见根因）
openclaw plugins enable discord

# 2. 修复proxy配置（WSL2特有）
# 编辑 ~/.openclaw/openclaw.json，将 discord.proxy 改为 http://192.168.1.33:7897
# 或通过命令：
openclaw config set channels.discord.proxy "http://192.168.1.33:7897"

# 3. 重启Gateway
systemctl --user restart openclaw-gateway
```

**关键教训**：
- Discord是内置channel，但需要plugin启用
- `plugins.allow`配置变更需要Gateway重启
- WSL2访问Windows代理必须用Windows宿主机IP（192.168.1.x），不能用127.0.0.1
- Gateway重启会等待当前操作完成，不能强制

### Proxy配置（WSL2专用）

| 环境 | 代理地址 |
|------|----------|
| Windows本机 | `http://127.0.0.1:7897` |
| WSL2访问Windows | `http://192.168.1.33:7897`（Windows宿主机IP） |

**获取Windows宿主机IP**：`ip route | grep default | awk '{print $3}'`（不一定准确）或 `hostname -I` 找到192.168.x.x网段的IP

---

## 系统当前缺陷（2026-03-27 03:20）

| # | 缺陷 | 严重度 | 状态 |
|---|------|--------|------|
| 1 | Discord丢失 | 中 | 📋 待处理 |
| 2 | rate_limiter卡住 | 中 | 📋 待处理 |
| 3 | 议会协议未激活 | 中 | 📋 待处理 |
| 4 | expert_tracker数据量少（仅3 experts） | 低 | 📋 待重建 |

**已解决（本次清理确认）**：
- .openclaw/centers symlink ✅
- ratings.json位置 ✅
- xuzhi_memory/centers/不存在（无需清理）✅
- GitHub remote大小写 ✅
- Git HEAD已更新 ✅
